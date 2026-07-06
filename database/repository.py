import sqlite3
import time
import os


DB_PATH = "bot.db"


class TradeRepository:

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.create_table()

    # ================================
    # TABLE 생성
    # ================================
    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            side TEXT,
            qty REAL,
            price REAL,
            pnl REAL,
            timestamp REAL
        )
        """)

        self.conn.commit()

    # ================================
    # TRADE INSERT
    # ================================
    def insert(self, symbol, side, qty, price, pnl):

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO trades (symbol, side, qty, price, pnl, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (symbol, side, qty, price, pnl, time.time()))

        self.conn.commit()

    # ================================
    # ALL TRADE GET
    # ================================
    def all(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM trades ORDER BY id DESC
        """)

        return cursor.fetchall()


# 글로벌 인스턴스
trade_db = TradeRepository()
