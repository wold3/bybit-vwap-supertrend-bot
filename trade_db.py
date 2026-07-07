import sqlite3
import os
import threading
import time



class TradeDB:


    def __init__(self):


        self.db_file = os.getenv(

            "TRADE_DB",

            "trades.db"

        )


        self.lock = threading.Lock()



        self.init_db()





    # =====================================
    # CREATE TABLE
    # =====================================

    def init_db(
        self
    ):


        with sqlite3.connect(
            self.db_file
        ) as conn:


            cursor = conn.cursor()



            cursor.execute(

                """

                CREATE TABLE IF NOT EXISTS trades

                (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    symbol TEXT,

                    side TEXT,

                    qty REAL,

                    price REAL,

                    pnl REAL DEFAULT 0,

                    trade_type TEXT,

                    timestamp REAL

                )

                """

            )



            conn.commit()





    # =====================================
    # INSERT TRADE
    # =====================================

    def insert(
        self,
        symbol,
        side,
        qty,
        price,
        pnl=0,
        trade_type="ENTRY"
    ):


        with self.lock:


            with sqlite3.connect(

                self.db_file

            ) as conn:


                cursor = conn.cursor()



                cursor.execute(

                    """

                    INSERT INTO trades

                    (

                    symbol,

                    side,

                    qty,

                    price,

                    pnl,

                    trade_type,

                    timestamp

                    )

                    VALUES(?,?,?,?,?,?,?)

                    """,

                    (

                        symbol,

                        side,

                        qty,

                        price,

                        pnl,

                        trade_type,

                        time.time()

                    )

                )



                conn.commit()





    # =====================================
    # RECENT TRADES
    # =====================================

    def get_recent(
        self,
        limit=100
    ):


        with sqlite3.connect(

            self.db_file

        ) as conn:


            cursor = conn.cursor()



            cursor.execute(

                """

                SELECT

                id,

                symbol,

                side,

                qty,

                price,

                pnl,

                trade_type,

                timestamp


                FROM trades

                ORDER BY id DESC

                LIMIT ?

                """,

                (

                    limit,

                )

            )



            rows = cursor.fetchall()



            result = []



            for r in rows:


                result.append({


                    "id":

                        r[0],


                    "symbol":

                        r[1],


                    "side":

                        r[2],


                    "qty":

                        r[3],


                    "price":

                        r[4],


                    "pnl":

                        r[5],


                    "type":

                        r[6],


                    "time":

                        r[7]


                })



            return result





    # =====================================
    # LAST TRADE
    # =====================================

    def last(
        self,
        symbol
    ):


        with sqlite3.connect(

            self.db_file

        ) as conn:


            cursor = conn.cursor()



            cursor.execute(

                """

                SELECT *

                FROM trades

                WHERE symbol=?

                ORDER BY id DESC

                LIMIT 1

                """,

                (

                    symbol,

                )

            )


            return cursor.fetchone()





trade_db = TradeDB()
