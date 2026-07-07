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
    # DATABASE INIT
    # =====================================

    def init_db(self):

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


            for row in rows:

                result.append(

                    {
                        "id": row[0],

                        "symbol": row[1],

                        "side": row[2],

                        "qty": row[3],

                        "price": row[4],

                        "pnl": row[5],

                        "type": row[6],

                        "time": row[7]
                    }

                )


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



    # =====================================
    # DELETE ALL (TEST)
    # =====================================

    def clear(self):

        with self.lock:

            with sqlite3.connect(
                self.db_file
            ) as conn:

                cursor = conn.cursor()

                cursor.execute(
                    "DELETE FROM trades"
                )

                conn.commit()



# =====================================
# SINGLETON
# =====================================

trade_db = TradeDB()
