# =====================================================
# database/database.py
# SQLite Trading Database
# =====================================================

import sqlite3
import threading
import os
from datetime import datetime



from config import DATABASE_PATH





class Database:


    def __init__(self):


        self.lock = threading.Lock()


        self.connection = None



        self.connect()


        self.create_tables()



        print(

            "[DATABASE READY]"

        )









    # =====================================================
    # CONNECT
    # =====================================================

    def connect(self):


        folder = os.path.dirname(

            DATABASE_PATH

        )



        if folder and not os.path.exists(folder):


            os.makedirs(folder)





        self.connection = sqlite3.connect(


            DATABASE_PATH,


            check_same_thread=False


        )





    # =====================================================
    # TABLE
    # =====================================================

    def create_tables(self):


        with self.lock:


            cursor = self.connection.cursor()





            cursor.execute("""


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






            cursor.execute("""


            CREATE TABLE IF NOT EXISTS errors (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                time TEXT,

                message TEXT

            )


            """)





            self.connection.commit()







    # =====================================================
    # SAVE TRADE
    # =====================================================

    def save_trade(

        self,

        symbol,

        side,

        qty,

        price,

        pnl=0

    ):


        try:


            with self.lock:


                cursor = self.connection.cursor()



                cursor.execute("""


                INSERT INTO trades

                (

                time,

                symbol,

                side,

                qty,

                price,

                pnl

                )

                VALUES (?,?,?,?,?,?)


                """,

                (

                    datetime.now().strftime(

                        "%Y-%m-%d %H:%M:%S"

                    ),

                    symbol,

                    side,

                    qty,

                    price,

                    pnl

                ))



                self.connection.commit()






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


            if self.connection is None:


                return





            with self.lock:


                cursor = self.connection.cursor()



                cursor.execute("""


                INSERT INTO errors

                (

                time,

                message

                )

                VALUES (?,?)


                """,

                (

                    datetime.now().strftime(

                        "%Y-%m-%d %H:%M:%S"

                    ),

                    str(error)

                ))



                self.connection.commit()





        except Exception as e:


            print(

                "[SAVE ERROR FAILED]",

                e

            )









    # =====================================================
    # GET TRADES
    # =====================================================

    def get_trades(

        self,

        limit=100

    ):


        try:


            with self.lock:


                cursor = self.connection.cursor()



                cursor.execute("""


                SELECT *

                FROM trades

                ORDER BY id DESC

                LIMIT ?


                """,

                (

                    limit,

                ))



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


            if self.connection:


                self.connection.close()



                self.connection = None



            print(

                "[DATABASE CLOSED]"

            )





        except Exception as e:


            print(

                "[DATABASE CLOSE ERROR]",

                e

            )









# =====================================================
# INSTANCE
# =====================================================

database = Database()
