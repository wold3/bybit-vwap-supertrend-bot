# =====================================================
# database/database.py
# SQLite Database Manager
# =====================================================


import sqlite3
import os
import threading
import time



from config import (
    DATABASE_FILE
)





class Database:



    def __init__(self):


        self.lock = threading.Lock()


        folder = os.path.dirname(

            DATABASE_FILE

        )



        if folder:


            os.makedirs(

                folder,

                exist_ok=True

            )





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

        CREATE TABLE IF NOT EXISTS errors

        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            time TEXT,

            error TEXT

        )

        """

        )





        cursor.execute(

        """

        CREATE TABLE IF NOT EXISTS orders

        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            time TEXT,

            symbol TEXT,

            side TEXT,

            qty REAL,

            price REAL,

            status TEXT

        )

        """

        )







        cursor.execute(

        """

        CREATE TABLE IF NOT EXISTS logs

        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            time TEXT,

            message TEXT

        )

        """

        )






        self.conn.commit()







    # =====================================================
    # ERROR
    # =====================================================

    def save_error(
        self,
        error
    ):


        try:



            with self.lock:



                self.conn.execute(

                """

                INSERT INTO errors

                (

                    time,

                    error

                )

                VALUES (?,?)

                """,

                (

                    time.strftime(

                        "%Y-%m-%d %H:%M:%S"

                    ),

                    str(error)

                )

                )



                self.conn.commit()





        except Exception as e:



            print(

                "[DB ERROR]",

                e

            )









    # =====================================================
    # ORDER LOG
    # =====================================================

    def save_order(
        self,
        symbol,
        side,
        qty,
        price,
        status
    ):


        try:



            with self.lock:



                self.conn.execute(

                """

                INSERT INTO orders

                (

                    time,

                    symbol,

                    side,

                    qty,

                    price,

                    status

                )

                VALUES (?,?,?,?,?,?)

                """,

                (

                    time.strftime(

                        "%Y-%m-%d %H:%M:%S"

                    ),

                    symbol,

                    side,

                    qty,

                    price,

                    status

                )

                )



                self.conn.commit()





        except Exception as e:



            print(

                "[DB ORDER ERROR]",

                e

            )









    # =====================================================
    # LOG
    # =====================================================

    def save_log(
        self,
        message
    ):


        try:



            with self.lock:



                self.conn.execute(

                """

                INSERT INTO logs

                (

                    time,

                    message

                )

                VALUES (?,?)

                """,

                (

                    time.strftime(

                        "%Y-%m-%d %H:%M:%S"

                    ),

                    str(message)

                )

                )



                self.conn.commit()





        except Exception as e:



            print(

                "[DB LOG ERROR]",

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
