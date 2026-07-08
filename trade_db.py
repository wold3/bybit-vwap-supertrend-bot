import sqlite3
import threading
from pathlib import Path


class TradeDB:
    """
    Trade Database

    기능
    - 거래내역 저장
    - 거래내역 조회
    """

    def __init__(self):

        self.lock = threading.Lock()

        self.db_path = Path("trade_history.db")

        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        self._create_table()


    # =====================================
    # CREATE TABLE
    # =====================================

    def _create_table(self):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trades (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    symbol TEXT,

                    side TEXT,

                    qty REAL,

                    price REAL,

                    pnl REAL,

                    trade_type TEXT,

                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                )
            """)

            self.conn.commit()


    # =====================================
    # INSERT
    # =====================================

    def insert(
        self,
        symbol,
        side,
        qty,
        price,
        pnl,
        trade_type
    ):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                """
                INSERT INTO trades
                (
                    symbol,
                    side,
                    qty,
                    price,
                    pnl,
                    trade_type
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    symbol,
                    side,
                    qty,
                    price,
                    pnl,
                    trade_type
                )
            )

            self.conn.commit()

        return True


    # =====================================
    # GET ALL
    # =====================================

    def get_all(self):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                "SELECT * FROM trades ORDER BY id DESC"
            )

            return cursor.fetchall()


    # =====================================
    # COUNT
    # =====================================

    def count(self):

        with self.lock:

            cursor = self.conn.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM trades"
            )

            return cursor.fetchone()[0]


    # =====================================
    # CLOSE
    # =====================================

    def close(self):

        self.conn.close()


# singleton
trade_db = TradeDB()
