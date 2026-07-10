# =====================================================
# database/database.py
# SQLite Trading Database
# =====================================================

import sqlite3
import threading
import time
import json
import os



from config import (
    DATABASE_PATH
)







class Database:



    def __init__(self):


        self.lock = threading.Lock()


        self.path = DATABASE_PATH



        self.initialize()



        print(
            "[DATABASE READY]"
        )







    # =====================================================
    # CONNECT
    # =====================================================

    def connect(self):


        folder = os.path.dirname(

            self.path

        )


        if folder:


            os.makedirs(

                folder,

                exist_ok=True

            )



        return sqlite3.connect(

            self.path,

            check_same_thread=False

        )







    # =====================================================
    # INIT TABLE
    # =====================================================

    def initialize(self):


        with self.lock:


            conn = self.connect()


            cur = conn.cursor()



            cur.execute(

                """
                CREATE TABLE IF NOT EXISTS events
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time REAL,
                    event TEXT
                )
                """

            )



            cur.execute(

                """
                CREATE TABLE IF NOT EXISTS errors
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time REAL,
                    error TEXT
                )
                """

            )



            cur.execute(

                """
                CREATE TABLE IF NOT EXISTS signals
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time REAL,
                    data TEXT
                )
                """

            )



            cur.execute(

                """
                CREATE TABLE IF NOT EXISTS orders
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    time REAL,
                    side TEXT,
                    qty REAL,
                    result TEXT
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


                conn.execute(

                    """
                    INSERT INTO events
                    VALUES
                    (
                    NULL,
                    ?,
                    ?
                    )
                    """,

                    (

                        time.time(),

                        text

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
    # ERROR
    # =====================================================

    def save_error(
        self,
        error
    ):


        try:


            with self.lock:


                conn = self.connect()



                conn.execute(

                    """
                    INSERT INTO errors
                    VALUES
                    (
                    NULL,
                    ?,
                    ?
                    )
                    """,

                    (

                        time.time(),

                        str(error)

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
    # SIGNAL
    # =====================================================

    def save_signal(
        self,
        signal
    ):


        try:


            with self.lock:


                conn = self.connect()



                conn.execute(

                    """
                    INSERT INTO signals
                    VALUES
                    (
                    NULL,
                    ?,
                    ?
                    )
                    """,

                    (

                        time.time(),

                        json.dumps(

                            signal,

                            ensure_ascii=False

                        )

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



                conn.execute(

                    """
                    INSERT INTO orders
                    VALUES
                    (
                    NULL,
                    ?,
                    ?,
                    ?,
                    ?
                    )
                    """,

                    (

                        time.time(),

                        side,

                        qty,

                        json.dumps(

                            result,

                            ensure_ascii=False

                        )

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
    # READ LAST EVENTS
    # =====================================================

    def recent_events(
        self,
        limit=20
    ):


        conn = self.connect()



        rows = conn.execute(

            """
            SELECT *
            FROM events
            ORDER BY id DESC
            LIMIT ?
            """,

            (

                limit,

            )

        ).fetchall()



        conn.close()



        return rows







    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "database":

                self.path,


            "ready":

                True


        }








# =====================================================
# SINGLETON
# =====================================================

database = Database()
