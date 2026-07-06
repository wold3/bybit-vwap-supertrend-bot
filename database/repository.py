import sqlite3
import time


DB_PATH = "bot.db"


class TradeRepository:

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.create_tables()

    # ================================
    # TABLE 생성
    # ================================
    def create_tables(self):

        cursor = self.conn.cursor()

        # 거래 테이블
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

        # PnL 히스토리 테이블 (핵심)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pnl_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    # ALL TRADES
    # ================================
    def all(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT * FROM trades ORDER BY id DESC
        """)

        return cursor.fetchall()

    # ================================
    # PnL HISTORY INSERT
    # ================================
    def insert_pnl_history(self, pnl):

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO pnl_history (pnl, timestamp)
            VALUES (?, ?)
        """, (pnl, time.time()))

        self.conn.commit()

    # ================================
    # PnL HISTORY GET
    # ================================
    def get_pnl_history(self, limit=200):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT pnl, timestamp
            FROM pnl_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

        rows = cursor.fetchall()

        return rows[::-1]


# 글로벌 인스턴스
trade_db = TradeRepository()
