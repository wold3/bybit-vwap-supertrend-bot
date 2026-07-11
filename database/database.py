# =====================================================
# database/database.py
# Trading Database Manager
# =====================================================

import sqlite3
import os
import threading
import time


from config import (
    DATABASE_FILE
)





class Database:


    def __init__(self):


        self.conn = None


        self.lock = threading.Lock()


        self.connect()


        self.create_tables()



        print(

            "[DATABASE READY]"

        )









    # =====================================================
    # CONNECT
    # =====================================================


    def connect(self):


        folder = os.path.dirname(

            DATABASE_FILE

        )


        if folder:


            os.makedirs(

                folder,

                exist_ok=True

            )



        self.conn = sqlite3.connect(

            DATABASE_FILE,

            check_same_thread=False

        )



        self.conn.row_factory = sqlite3.Row







    # =====================================================
    # TABLES
    # =====================================================


    def create_tables(self):


        with self.lock:


            cur = self.conn.cursor()



            cur.execute(
"""
CREATE TABLE IF NOT EXISTS trades
(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 time TEXT,
 symbol TEXT,
 side TEXT,
 qty REAL,
 entry REAL,
 tp REAL,
 sl REAL,
 result TEXT
)
"""
            )





            cur.execute(
"""
CREATE TABLE IF NOT EXISTS logs
(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 time TEXT,
 message TEXT
)
"""
            )





            cur.execute(
"""
CREATE TABLE IF NOT EXISTS errors
(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 time TEXT,
 error TEXT
)
"""
            )



            self.conn.commit()







    # =====================================================
    # SAVE TRADE
    # =====================================================


    def save_trade(
        self,
        trade
    ):


        try:


            with self.lock:


                cur = self.conn.cursor()



                cur.execute(
"""
INSERT INTO trades
(
time,
symbol,
side,
qty,
entry,
tp,
sl,
result
)

VALUES
(
?,?,?,?,?,?,?,?
)
""",

(
time.strftime(
"%Y-%m-%d %H:%M:%S"
),

trade.get("symbol"),

trade.get("side"),

trade.get("qty"),

trade.get("entry"),

trade.get("tp"),

trade.get("sl"),

trade.get("result")

)

                )



                self.conn.commit()





        except Exception as e:


            print(

                "[DB TRADE ERROR]",

                e

            )









    # =====================================================
    # SAVE LOG
    # =====================================================


    def save_log(
        self,
        message
    ):


        try:


            with self.lock:


                self.conn.execute(
"""
INSERT INTO logs
(
time,
message
)

VALUES
(
?,
?
)
""",

(

time.strftime(

"%Y-%m-%d %H:%M:%S"

),

str(message)

)

                )


                self.conn.commit()




        except Exception as e:


            print(

                "[DB LOG ERROR]",

                e

            )









    # =====================================================
    # SAVE ERROR
    # =====================================================


    def save_error(
        self,
        error
    ):


        try:


            with self.lock:


                self.conn.execute(
"""
INSERT INTO errors
(
time,
error
)

VALUES
(
?,
?
)
""",

(

time.strftime(

"%Y-%m-%d %H:%M:%S"

),

str(error)

)

                )



                self.conn.commit()





        except Exception as e:


            print(

                "[DB ERROR]",

                e

            )









    # =====================================================
    # RECENT TRADES
    # =====================================================


    def get_recent_trades(
        self,
        limit=50
    ):


        try:


            cur = self.conn.cursor()



            rows = cur.execute(
"""
SELECT *

FROM trades

ORDER BY id DESC

LIMIT ?
""",

(
limit,
)

            ).fetchall()



            return [

                dict(r)

                for r in rows

            ]



        except:


            return []









    # =====================================================
    # STATISTICS
    # =====================================================


    def get_trade_stats(self):


        try:


            cur = self.conn.cursor()



            total = cur.execute(
"""
SELECT COUNT(*) FROM trades
"""
            ).fetchone()[0]



            wins = cur.execute(
"""
SELECT COUNT(*)

FROM trades

WHERE result='WIN'
"""
            ).fetchone()[0]



            winrate = 0



            if total > 0:


                winrate = (

                    wins /

                    total *

                    100

                )



            return {


                "trades":

                    total,


                "wins":

                    wins,


                "winrate":

                    round(

                        winrate,

                        2

                    )

            }




        except:


            return {}









    # =====================================================
    # CLOSE
    # =====================================================


    def close(self):


        try:


            if self.conn:


                self.conn.close()



                self.conn = None



                print(

                    "[DATABASE CLOSED]"

                )



        except Exception as e:


            print(

                "[DB CLOSE ERROR]",

                e

            )









# =====================================================
# INSTANCE
# =====================================================


database = Database()
