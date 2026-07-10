# =====================================================
# database/database.py
# SQLite Database Manager
# =====================================================

import sqlite3
import threading
import os
import time



from config import (
    DATABASE_PATH
)







class Database:



    def __init__(self):


        self.lock = threading.Lock()



        folder = os.path.dirname(

            DATABASE_PATH

        )



        if folder:


            os.makedirs(

                folder,

                exist_ok=True

            )



        self.create_tables()



        print(

            "[DATABASE READY]"

        )







    # =====================================================
    # CONNECTION
    # =====================================================

    def connect(self):


        return sqlite3.connect(

            DATABASE_PATH,

            check_same_thread=False

        )







    # =====================================================
    # TABLE CREATE
    # =====================================================

    def create_tables(self):


        with self.lock:


            conn = self.connect()


            cur = conn.cursor()



            cur.execute(

                """

                CREATE TABLE IF NOT EXISTS events
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event TEXT,
                    created REAL
                )

                """

            )



            cur.execute(

                """

                CREATE TABLE IF NOT EXISTS signals
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    signal TEXT,
                    price REAL,
                    created REAL
                )

                """

            )



            cur.execute(

                """

                CREATE TABLE IF NOT EXISTS orders
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    side TEXT,
                    qty REAL,
                    result TEXT,
                    created REAL
                )

                """

            )



            cur.execute(

                """

                CREATE TABLE IF NOT EXISTS errors
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    error TEXT,
                    created REAL
                )

                """

            )



            conn.commit()


            conn.close()







    # =====================================================
    # EVENT
    # =====================================================

    def event(
        self,
        text
    ):


        try:


            with self.lock:


                conn = self.connect()


                cur = conn.cursor()



                cur.execute(

                    """

                    INSERT INTO events
                    (
                        event,
                        created
                    )

                    VALUES
                    (?,?)

                    """,

                    (

                        text,

                        time.time()

                    )

                )



                conn.commit()


                conn.close()



        except Exception as e:


            print(

                "[DB EVENT ERROR]",

                e

            )







    # =====================================================
    # SIGNAL
    # =====================================================

    def save_signal(
        self,
        signal
    ):


        try:


            with self.lock:


                conn = self.connect()


                cur = conn.cursor()



                cur.execute(

                    """

                    INSERT INTO signals
                    (
                        signal,
                        price,
                        created
                    )

                    VALUES
                    (?,?,?)

                    """,

                    (

                        signal.get(

                            "signal"

                        ),


                        signal.get(

                            "price",

                            0

                        ),


                        time.time()

                    )

                )



                conn.commit()


                conn.close()



        except Exception as e:


            print(

                "[DB SIGNAL ERROR]",

                e

            )







    # =====================================================
    # ORDER
    # =====================================================

    def save_order(
        self,
        side,
        qty,
        result
    ):


        try:


            with self.lock:


                conn = self.connect()


                cur = conn.cursor()



                cur.execute(

                    """

                    INSERT INTO orders
                    (
                        side,
                        qty,
                        result,
                        created
                    )

                    VALUES
                    (?,?,?,?)

                    """,

                    (

                        side,

                        qty,

                        str(result),

                        time.time()

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
    # ERROR
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

                        time.time()

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
    # STATUS
    # =====================================================

    def status(self):


        return {


            "database":

                DATABASE_PATH,


            "ready":

                True


        }







# =====================================================
# SINGLETON
# =====================================================

database = Database()
