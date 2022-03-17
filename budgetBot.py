from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import datetime;
import sqlite3

updater = Updater("5121747527:AAHAqxa5OAggkBTVyDf6Ee-eirzSPTKRxGE", use_context=True)
valid_userIDs = [1126312806]

def validUser(update):
    try:
        return update.message.from_user['id'] in valid_userIDs
    except:
        return False


def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user['id']
    update.message.reply_text( """Hiya, I am BUDget.bot.
    Available Commands :-
    /add <product_name,price,category> - To add an expense to the book
    /buy <name> - To add an item to the ToBuy list""")
    update.message.reply_text(user_id )

def initDB():
    with sqlite3.connect("expenses.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS expenses (
        id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL,
        amount decimal (10,2) NOT NULL,
        category text NOT NULL,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP);""")

        cur.execute("""CREATE TABLE IF NOT EXISTS toBuy (
        id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL,
        created_at timestamp DEFAULT CURRENT_TIMESTAMP);""")

def addExpenseToDB(name: str, amount: float, category: str):
    with sqlite3.connect("expenses.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)", (name, amount, category));

def addToBuyToDB(name: str):
    with sqlite3.connect("expenses.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO toBuy (name) VALUES (?)", (name));

def getExpensesFromDB():
    with sqlite3.connect("expenses.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM expenses")
        rows = cur.fetchall()
        allRows = "All expenses:\n"
        for row in rows:
            print(row)
            allRows+='\t'.join([str(value) for value in row])+'\n'
        return allRows

def addExpense(update: Update, context: CallbackContext):
    try:
        if validUser(update):
            name, cost, category = update.message.text.split(" ")[1].split(",")
            date = datetime.datetime.now()
            update.message.reply_text("adding '%s' price: %s, category: %s to the expense list\ndate:%s" % (name, cost, category, date))
            addExpenseToDB(name, cost, category)
            update.message.reply_text(getExpensesFromDB())
        else:
            update.message.reply_text("Invalid user, this user is not authorized to use this bot.")
    except Exception as e:
        print(e)
        update.message.reply_text("/add <product_name;price;category> - To add an expense to the book")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /add <product_name;price;category> - To add an expense to the book
    /buy <name> - To add an item to the ToBuy list""")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
    "Please write /help to see the commands available.")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
    "Sorry I can't recognize you , you said '%s'" % update.message.text)

initDB()
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('add', addExpense, pass_args=True))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
