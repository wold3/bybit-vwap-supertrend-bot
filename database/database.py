# =====================================================
# database/database.py
# Trading Database Manager
# =====================================================

import sqlite3
import threading
import os
import time


from config import DATABASE_FILE





class Database:



    def __init__(self):


        self.lock = threading.Lock()


        self.path = DATABASE_FILE



        self.create_folder()


        self.init_db()



        print(

            "[DATABASE READY]"

        )









    # =====================================================
    # FOLDER
    # =====================================================

    def create_folder(self):


        folder = os.path.dirname(

            self.path

        )


        if folder:


            os.makedirs(

                folder,

                exist_ok=True

            )









    # =====================================================
    # CONNECTION
    # =====================================================

    def connect(self):


        return sqlite3.connect(

            self.path,

            check_same_thread=False

        )









    # =====================================================
    # INIT TABLE
    # =====================================================

    def init_db(self):


        with self.lock:


            conn = self.connect()

            cur = conn.cursor()





            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS trades
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT,

                side TEXT,

                price REAL,

                qty REAL,

                pnl REAL DEFAULT 0,

                created INTEGER
            )
            """
            )





            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS orders
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                order_id TEXT,

                symbol TEXT,

                side TEXT,

                qty REAL,

                status TEXT,

                created INTEGER
            )
            """
            )







            cur.execute(
            """
            CREATE TABLE IF NOT EXISTS errors
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                error TEXT,

                created INTEGER
            )
            """
            )





            conn.commit()


            conn.close()







    # =====================================================
    # SAVE TRADE
    # =====================================================

    def save_trade(
        self,
        symbol,
        side,
        price,
        qty,
        pnl=0
    ):


        try:


            with self.lock:


                conn = self.connect()

                cur = conn.cursor()



                cur.execute(
                """
                INSERT INTO trades
                (
                    symbol,
                    side,
                    price,
                    qty,
                    pnl,
                    created
                )

                VALUES
                (?,?,?,?,?,?)
                """,

                (
                    symbol,
                    side,
                    price,
                    qty,
                    pnl,
                    int(time.time())

                )

                )



                conn.commit()

                conn.close()



        except Exception as e:


            print(

                "[DB TRADE ERROR]",

                e

            )









    # =====================================================
    # SAVE ORDER
    # =====================================================

    def save_order(
        self,
        order_id,
        symbol,
        side,
        qty,
        status
    ):


        try:


            with self.lock:


                conn = self.connect()

                cur = conn.cursor()



                cur.execute(
                """
                INSERT INTO orders
                (
                    order_id,
                    symbol,
                    side,
                    qty,
                    status,
                    created
                )

                VALUES
                (?,?,?,?,?,?)
                """,

                (
                    order_id,
                    symbol,
                    side,
                    qty,
                    status,
                    int(time.time())

                )

                )



                conn.commit()

                conn.close()





        except Exception as e:


            print(

                "[DB ORDER ERROR]",

                e

            )











    # =====================================================
    # SAVE ERROR
    # =====================================================

    def save_error(
        self,
        error
    ):


        try:


            with self.lock:


                conn = self.connect()

                cur = conn.cursor()



                cur.execute(
                """
                INSERT INTO errors
                (
                    error,
                    created
                )

                VALUES
                (?,?)
                """,

                (

                    str(error),

                    int(time.time())

                )

                )



                conn.commit()

                conn.close()





        except Exception as e:


            print(

                "[DB ERROR]",

                e

            )











    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):


        print(

            "[DATABASE CLOSED]"

        )









# =====================================================
# SINGLETON
# =====================================================

database = Database()
