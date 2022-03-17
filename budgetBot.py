from userHelper import UserHelper
from dbHelper import DBHelper
from telegramHelper import TelegramHelper

db = DBHelper("expenses.db")
userHelper = UserHelper()
telegramBot = TelegramHelper(db, userHelper)
telegramBot.start_polling()