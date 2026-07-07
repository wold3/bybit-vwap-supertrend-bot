import sqlite3
import time


class TradeDB:


    def __init__(self):

        self.conn = sqlite3.connect(

            "trades.db",

            check_same_thread=False

        )


        self.create()



    def create(self):

        cur = self.conn.cursor()


        cur.execute("""

        CREATE TABLE IF NOT EXISTS trades(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            symbol TEXT,

            side TEXT,

            qty REAL,

            price REAL,

            pnl REAL DEFAULT 0,

            created REAL

        )

        """)


        self.conn.commit()



    # ==========================
    # INSERT
    # ==========================

    def insert(
        self,
        symbol,
        side,
        qty,
        price
    ):


        cur = self.conn.cursor()


        cur.execute("""

        INSERT INTO trades
        (
            symbol,
            side,
            qty,
            price,
            created
        )

        VALUES (?,?,?,?,?)

        """,

        (

            symbol,

            side,

            qty,

            price,

            time.time()

        ))


        self.conn.commit()



    # ==========================
    # ALL
    # ==========================

    def all(self):

        cur = self.conn.cursor()


        cur.execute("""

        SELECT *

        FROM trades

        ORDER BY id DESC

        LIMIT 100

        """)


        return cur.fetchall()



trade_db = TradeDB()
