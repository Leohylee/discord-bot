import sqlite3
from sqlite3 import Error

DB_PATH = "DiscordBot.db"


class User_Messages:
    swear = []
    dot = []
    csgo = []

    def __init__(self):
        try:
            db_conn = sqlite3.connect(DB_PATH)
            db_cur = db_conn.cursor()
            db_cur.execute("SELECT * FROM User_Message")
            results = db_cur.fetchall()
        except Error as e:
            print(e)
        for row in results:
            match row[0]:
                case "csgo":
                    self.csgo.append(row[1])
                case "dot":
                    self.dot.append(row[1])
                case "swear":
                    self.swear.append(row[1])
