from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import datetime;

class TelegramHelper:
    def __init__(self, db, userHelper, configFile="telegram.conf"):
        with open(configFile) as file:
            self.token = file.read()
        self.db = db
        self.userHelper = userHelper

        self.updater = Updater(self.token, use_context=True)
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help))
        self.updater.dispatcher.add_handler(CommandHandler('add', self.addExpense, pass_args=True))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.unknown))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.command, self.unknown)) # Filters out unknown commands
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.unknown_text))   # Filters unknown Texts
    
    def start(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user['id']
        update.message.reply_text( """Hiya, I am BUDget.bot.
            Available Commands :-
            /add <product_name,price,category> - To add an expense to the book
            /buy <name> - To add an item to the ToBuy list""")
        update.message.reply_text(user_id )

    def addExpense(self, update: Update, context: CallbackContext):
        try:
            if self.userHelper.validUser(update):
                name, cost, category = update.message.text.split(" ")[1].split(",")
                date = datetime.datetime.now()
                update.message.reply_text("adding '%s' price: %s, category: %s to the expense list\ndate:%s" % (name, cost, category, date))
                self.db.addExpenseToDB(name, cost, category)
                update.message.reply_text(self.db.getExpensesFromDB())
            else:
                update.message.reply_text("Invalid user, this user is not authorized to use this bot.")
        except Exception as e:
            print(e)
            update.message.reply_text("/add <product_name;price;category> - To add an expense to the book")

    def help(self, update: Update, context: CallbackContext):
        update.message.reply_text("""Available Commands :-
        /add <product_name;price;category> - To add an expense to the book
        /buy <name> - To add an item to the ToBuy list""")

    def unknown(self, update: Update, context: CallbackContext):
        update.message.reply_text(
        "Please write /help to see the commands available.")

    def unknown_text(self, update: Update, context: CallbackContext):
        update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)

    def start_polling(self):
        self.updater.start_polling()