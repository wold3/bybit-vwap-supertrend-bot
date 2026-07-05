import sqlite3
from datetime import datetime

DB_PATH = "trades.db"


def init_db():
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


def insert_trade(symbol, side, qty, price, pnl=0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO trades (time, symbol, side, qty, price, pnl)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        symbol,
        side,
        qty,
        price,
        pnl
    ))

    conn.commit()
    conn.close()


def get_trades(limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        SELECT * FROM trades
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = c.fetchall()
    conn.close()

    return rows
