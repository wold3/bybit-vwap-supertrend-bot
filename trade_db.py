import sqlite3


class TradeDB:

    def __init__(self):

        self.conn = sqlite3.connect("trades.db", check_same_thread=False)
        self.init_db()

    # =================================================
    # INIT
    # =================================================
    def init_db(self):

        c = self.conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                side TEXT,
                qty REAL,
                price REAL,
                pnl REAL,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS equity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equity REAL,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.conn.commit()

    # =================================================
    # TRADE INSERT
    # =================================================
    def insert(self, symbol, side, qty, price, pnl):

        c = self.conn.cursor()

        c.execute("""
            INSERT INTO trades (symbol, side, qty, price, pnl)
            VALUES (?, ?, ?, ?, ?)
        """, (symbol, side, qty, price, pnl))

        self.conn.commit()

    # =================================================
    # EQUITY INSERT
    # =================================================
    def insert_equity(self, equity):

        c = self.conn.cursor()

        c.execute("""
            INSERT INTO equity (equity)
            VALUES (?)
        """, (equity,))

        self.conn.commit()

    # =================================================
    # GET TRADES
    # =================================================
    def all(self):

        c = self.conn.cursor()
        c.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 100")
        return c.fetchall()

    # =================================================
    # EQUITY HISTORY
    # =================================================
    def get_equity_history(self):

        c = self.conn.cursor()
        c.execute("SELECT equity, time FROM equity ORDER BY id ASC")
        return c.fetchall()


# SINGLETON
trade_db = TradeDB()
