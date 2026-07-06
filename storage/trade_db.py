import sqlite3
from datetime import datetime


class TradeDB:

    def __init__(self):

        self.conn = sqlite3.connect("trades.db", check_same_thread=False)
        self.create()

    def create(self):

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            side TEXT,
            qty REAL,
            price REAL,
            pnl REAL,
            time TEXT
        )
        """)
        self.conn.commit()

    # ================================
    # SAVE TRADE
    # ================================
    def save(self, symbol, side, qty, price, pnl):

        self.conn.execute("""
        INSERT INTO trades (symbol, side, qty, price, pnl, time)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (symbol, side, qty, price, pnl, datetime.utcnow().isoformat()))

        self.conn.commit()

    # ================================
    # GET ALL
    # ================================
    def all(self):

        cursor = self.conn.execute("SELECT * FROM trades")
        return cursor.fetchall()


trade_db = TradeDB()
