import sqlite3
from datetime import datetime


DB_PATH = "trades.db"


class TradeDB:

    def __init__(self):
        self.init_db()


    def init_db(self):

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            symbol TEXT,
            side TEXT,
            qty REAL,
            price REAL,
            pnl REAL
        )
        """)

        conn.commit()
        conn.close()



    def insert_trade(
        self,
        symbol,
        side,
        qty,
        price,
        pnl=0
    ):

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        INSERT INTO trades
        (
            time,
            symbol,
            side,
            qty,
            price,
            pnl
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.utcnow().isoformat(),
            symbol,
            side,
            qty,
            price,
            pnl
        ))

        conn.commit()
        conn.close()



    def get_recent_trades(
        self,
        limit=50
    ):

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        c = conn.cursor()

        c.execute("""
        SELECT *
        FROM trades
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,))

        rows = c.fetchall()

        conn.close()

        return [
            dict(row)
            for row in rows
        ]



    # dashboard/app.py 호환용
    def get_recent(
        self,
        limit=50
    ):

        return self.get_recent_trades(limit)



    def get_summary(self):

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(pnl),0)
        FROM trades
        """)

        row = c.fetchone()

        conn.close()

        return {
            "total_trades": row[0],
            "total_pnl": row[1]
        }



    def get_all(self):

        return self.get_recent_trades(1000)



# dashboard에서 사용하는 객체
trade_db = TradeDB()
