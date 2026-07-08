import sqlite3
import threading
from pathlib import Path



class TradeDB:
    """
    Trade Database

    기능:
    - Entry 기록
    - Exit 기록
    - PNL 기록
    - 거래 조회
    """



    def __init__(self):

        self.lock = threading.Lock()


        self.db_path = Path(

            "trade_history.db"

        )


        self.conn = sqlite3.connect(

            self.db_path,

            check_same_thread=False

        )


        self._create_table()





    # =====================================
    # TABLE
    # =====================================

    def _create_table(self):


        with self.lock:


            cursor = self.conn.cursor()



            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS trades
                (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    symbol TEXT NOT NULL,

                    side TEXT,

                    qty REAL,

                    entry_price REAL,

                    exit_price REAL,

                    pnl REAL DEFAULT 0,

                    trade_type TEXT,

                    created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP

                )
                """
            )



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
        pnl=0,
        trade_type="ENTRY"
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
                    entry_price,
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
    # COMPATIBILITY
    # =====================================

    def insert_trade(
        self,
        symbol,
        side,
        qty,
        price,
        pnl=0,
        trade_type="ENTRY"
    ):


        return self.insert(

            symbol,

            side,

            qty,

            price,

            pnl,

            trade_type

        )





    # =====================================
    # GET ALL
    # =====================================

    def get_all(self):


        with self.lock:


            cursor = self.conn.cursor()



            cursor.execute(
                """
                SELECT *
                FROM trades
                ORDER BY id DESC
                """
            )



            return cursor.fetchall()





    # =====================================
    # RECENT
    # =====================================

    def get_recent(
        self,
        limit=50
    ):


        with self.lock:


            cursor = self.conn.cursor()



            cursor.execute(
                """
                SELECT *
                FROM trades
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    limit,

                )
            )



            return cursor.fetchall()





    # =====================================
    # COUNT
    # =====================================

    def count(self):


        with self.lock:


            cursor = self.conn.cursor()



            cursor.execute(
                """
                SELECT COUNT(*)
                FROM trades
                """
            )


            return cursor.fetchone()[0]





    # =====================================
    # CLOSE
    # =====================================

    def close(self):

        with self.lock:

            self.conn.close()





# singleton

trade_db = TradeDB()
