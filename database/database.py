# database/database.py


import sqlite3
import threading



class Database:


    def __init__(self):


        self.path = "bot.db"

        self.lock = threading.Lock()


        self.init_db()



    # =====================================
    # INIT
    # =====================================

    def init_db(self):


        with self.lock:


            conn = sqlite3.connect(
                self.path
            )


            cursor = conn.cursor()



            cursor.execute("""

            CREATE TABLE IF NOT EXISTS trades (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT,

                side TEXT,

                qty REAL,

                entry REAL,

                exit REAL,

                pnl REAL,

                result TEXT,

                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

            )

            """)



            cursor.execute("""

            CREATE TABLE IF NOT EXISTS orders (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                order_id TEXT,

                side TEXT,

                qty REAL,

                price REAL,

                status TEXT,

                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

            )

            """)



            cursor.execute("""

            CREATE TABLE IF NOT EXISTS errors (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                message TEXT,

                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

            )

            """)



            conn.commit()

            conn.close()



    # =====================================
    # INSERT
    # =====================================

    def execute(
        self,
        query,
        params=()
    ):


        with self.lock:


            conn = sqlite3.connect(
                self.path
            )


            cursor = conn.cursor()


            cursor.execute(
                query,
                params
            )


            conn.commit()


            conn.close()




db = Database()
