# =====================================================
# database/database.py
# SQLite Trading Database
# =====================================================

import sqlite3
import threading
import os
import time


from config import (
    DATABASE_FILE
)





class Database:


    def __init__(self):


        self.conn = None


        self.lock = threading.Lock()


        self.connect()


        self.create_tables()


        print(

            "[DATABASE READY]"

        )









    # =====================================================
    # CONNECT
    # =====================================================


    def connect(self):


        try:


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



            self.conn.row_factory = sqlite3.Row





        except Exception as e:


            print(

                "[DATABASE CONNECT ERROR]",

                e

            )









    # =====================================================
    # TABLES
    # =====================================================


    def create_tables(self):


        with self.lock:


            cursor = self.conn.cursor()



            cursor.execute(

                """

                CREATE TABLE IF NOT EXISTS trades

                (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    time TEXT,

                    symbol TEXT,

                    side TEXT,

                    qty REAL,

                    entry REAL,

                    tp REAL,

                    sl REAL,

                    result TEXT

                )

                """

            )







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






            self.conn.commit()







    # =====================================================
    # SAVE TRADE
    # =====================================================


    def save_trade(
        self,
        data
    ):


        try:


            with self.lock:


                cursor = self.conn.cursor()



                cursor.execute(

                    """

                    INSERT INTO trades

                    (

                    time,

                    symbol,

                    side,

                    qty,

                    entry,

                    tp,

                    sl,

                    result

                    )

                    VALUES (?,?,?,?,?,?,?,?)

                    """,


                    (

                    time.strftime(

                        "%Y-%m-%d %H:%M:%S"

                    ),


                    data.get(

                        "symbol"

                    ),


                    data.get(

                        "side"

                    ),


                    data.get(

                        "qty"

                    ),


                    data.get(

                        "entry"

                    ),


                    data.get(

                        "tp"

                    ),


                    data.get(

                        "sl"

                    ),


                    data.get(

                        "result"

                    )

                    )

                )



                self.conn.commit()





                print(

                    "[TRADE SAVED]"

                )






        except Exception as e:


            print(

                "[SAVE TRADE ERROR]",

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


                cursor = self.conn.cursor()



                cursor.execute(

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

                "[SAVE ERROR FAILED]",

                e

            )









    # =====================================================
    # GET RECENT TRADES
    # =====================================================


    def get_trades(
        self,
        limit=50
    ):


        try:


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






        except Exception as e:


            print(

                "[GET TRADES ERROR]",

                e

            )


            return []









    # =====================================================
    # CLOSE
    # =====================================================


    def close(self):


        try:


            if self.conn:


                self.conn.close()



                print(

                    "[DATABASE CLOSED]"

                )



        except:


            pass









# =====================================================
# INSTANCE
# =====================================================


database = Database()
