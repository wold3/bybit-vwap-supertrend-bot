import sqlite3
from datetime import datetime


DB_PATH = "trades.db"


class TradeDB:

    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_db()


    def get_connection(self):
        return sqlite3.connect(self.db_path)


    def init_db(self):

        conn = self.get_connection()
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

        conn = self.get_connection()
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



    def get_recent_trades(self, limit=50):

        conn = self.get_connection()
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

        return rows



    def get_summary(self):

        conn = self.get_connection()
        c = conn.cursor()

        c.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(pnl),0)
        FROM trades
        """)

        result = c.fetchone()

        conn.close()

        return {
            "count": result[0],
            "pnl": result[1]
        }



# dashboard/app.py 에서 사용하는 객체
trade_db = TradeDB()



# 기존 함수 호출 호환용

def init_db():
    return trade_db.init_db()


def insert_trade(symbol, side, qty, price, pnl=0):
    return trade_db.insert_trade(
        symbol,
        side,
        qty,
        price,
        pnl
    )
