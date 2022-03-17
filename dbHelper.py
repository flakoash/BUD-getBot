import datetime;
import sqlite3

class DBHelper:
    def  __init__(self, dbName: str):
        self.dbName = dbName
        self.initDB()

    def execute(self, query:str, args=None):
        with sqlite3.connect(self.dbName) as con:
            cur = con.cursor()
            if args:
                return cur.execute(query, args)
            else:
                return cur.execute(query)

    def initDB(self):
        self.execute("""CREATE TABLE IF NOT EXISTS expenses (
            id integer PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL,
            amount decimal (10,2) NOT NULL,
            category text NOT NULL,
            created_at timestamp DEFAULT CURRENT_TIMESTAMP);""")

        self.execute("""CREATE TABLE IF NOT EXISTS toBuy (
            id integer PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL,
            created_at timestamp DEFAULT CURRENT_TIMESTAMP);""" )
    
    def addExpenseToDB(self, name: str, amount: float, category: str):
        self.execute("INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)", (name, amount, category))
    
    def addToBuyToDB(self, name: str):
        self.execute("INSERT INTO toBuy (name) VALUES (?)", (name))
    
    def getExpensesFromDB(self):
        rows = self.execute("SELECT * FROM expenses")
        allRows = "All expenses:\n"
        for row in rows:
            allRows+='\t'.join([str(value) for value in row])+'\n'
        return allRows
