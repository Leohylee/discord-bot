import sqlite3
from sqlite3 import Error

DB_PATH = "DiscordBot.db"


class Replies:
    greetings = []
    do_you_know = []
    csgo = []
    anti_swear = []
    flowers = []
    dot = []
    greeting_reply_type = ["greetings", "do_you_know", "cat"]
    greeting_weights = [60, 20, 20]

    def __init__(self):
        try:
            db_conn = sqlite3.connect(DB_PATH)
            db_cur = db_conn.cursor()
            db_cur.execute("SELECT * FROM Reply")
            results = db_cur.fetchall()
        except Error as e:
            print(e)
        for row in results:
            match row[0]:
                case "greetings":
                    self.greetings.append(row[1])
                case "do_you_know":
                    self.do_you_know.append(row[1])
                case "csgo":
                    self.csgo.append(row[1])
                case "anti_swear":
                    self.anti_swear.append(row[1])
                case "flowers":
                    self.flowers.append(row[1])
                case "dot":
                    self.dot.append(row[1])
