# =====================================================
# database/database.py
# Trading Bot SQLite Database
# =====================================================

import sqlite3
import threading
import time



from config import (
    DATABASE_FILE
)







class Database:



    def __init__(self):


        self.lock = threading.Lock()



        self.conn = sqlite3.connect(

            DATABASE_FILE,

            check_same_thread=False

        )



        self.create_tables()



        print(

            "[DATABASE READY]"

        )









    # =====================================================
    # TABLE INIT
    # =====================================================

    def create_tables(self):


        cursor = self.conn.cursor()



        cursor.execute(
            """

            CREATE TABLE IF NOT EXISTS events (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                time REAL,

                event TEXT

            )

            """
        )



        cursor.execute(
            """

            CREATE TABLE IF NOT EXISTS signals (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                time REAL,

                signal TEXT,

                price REAL,

                trend TEXT

            )

            """
        )



        cursor.execute(
            """

            CREATE TABLE IF NOT EXISTS trades (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                time REAL,

                side TEXT,

                qty REAL,

                pnl REAL

            )

            """
        )



        cursor.execute(
            """

            CREATE TABLE IF NOT EXISTS errors (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                time REAL,

                message TEXT

            )

            """
        )



        self.conn.commit()









    # =====================================================
    # EVENT
    # =====================================================

    def event(
        self,
        message
    ):


        try:


            with self.lock:


                self.conn.execute(

                    """

                    INSERT INTO events

                    (time,event)

                    VALUES (?,?)

                    """,

                    (

                        time.time(),

                        message

                    )

                )


                self.conn.commit()



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


                self.conn.execute(

                    """

                    INSERT INTO signals

                    (

                    time,

                    signal,

                    price,

                    trend

                    )

                    VALUES (?,?,?,?)

                    """,

                    (

                        time.time(),

                        signal.get(

                            "signal"

                        ),

                        signal.get(

                            "price",

                            0

                        ),

                        signal.get(

                            "trend"

                        )

                    )

                )


                self.conn.commit()



        except Exception as e:


            print(

                "[DB SIGNAL ERROR]",

                e

            )









    # =====================================================
    # TRADE
    # =====================================================

    def save_trade(
        self,
        side,
        qty,
        pnl=0
    ):


        try:


            with self.lock:


                self.conn.execute(

                    """

                    INSERT INTO trades

                    (

                    time,

                    side,

                    qty,

                    pnl

                    )

                    VALUES (?,?,?,?)

                    """,

                    (

                        time.time(),

                        side,

                        qty,

                        pnl

                    )

                )



                self.conn.commit()



        except Exception as e:


            print(

                "[DB TRADE ERROR]",

                e

            )











    # =====================================================
    # ERROR
    # =====================================================

    def save_error(
        self,
        message
    ):


        try:


            with self.lock:


                self.conn.execute(

                    """

                    INSERT INTO errors

                    (

                    time,

                    message

                    )

                    VALUES (?,?)

                    """,

                    (

                        time.time(),

                        str(message)

                    )

                )


                self.conn.commit()



        except Exception as e:


            print(

                "[DB ERROR]",

                e

            )









    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):


        try:


            self.conn.close()



        except:


            pass







# =====================================================
# SINGLETON
# =====================================================

database = Database()
