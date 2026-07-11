# =====================================================
# database/database.py
# SQLite Database Manager
# =====================================================

import sqlite3
import os
import time


from config import DATABASE_FILE





class Database:


    def __init__(self):


        folder = os.path.dirname(

            DATABASE_FILE

        )



        if folder and not os.path.exists(folder):


            os.makedirs(folder)



        self.conn = sqlite3.connect(

            DATABASE_FILE,

            check_same_thread=False

        )


        self.cursor = self.conn.cursor()



        self.create_tables()



        print(

            "[DATABASE READY]"

        )







    # =====================================================
    # TABLE CREATE
    # =====================================================


    def create_tables(self):


        self.cursor.execute(

        """

        CREATE TABLE IF NOT EXISTS errors

        (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            time TEXT,

            error TEXT

        )

        """

        )





        self.cursor.execute(

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





        self.cursor.execute(

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
    # ERROR SAVE
    # =====================================================


    def save_error(
        self,
        error
    ):


        try:


            self.cursor.execute(

            """

            INSERT INTO errors

            VALUES(NULL,?,?)

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
    # TRADE SAVE
    # =====================================================


    def save_trade(
        self,
        trade
    ):


        try:


            self.cursor.execute(

            """

            INSERT INTO trades

            VALUES(NULL,?,?,?,?,?,?,?,?)

            """,

            (

                time.strftime(

                    "%Y-%m-%d %H:%M:%S"

                ),


                trade.get(

                    "symbol",

                    ""

                ),


                trade.get(

                    "side",

                    ""

                ),


                float(

                    trade.get(

                        "qty",

                        0

                    )

                ),


                float(

                    trade.get(

                        "entry",

                        0

                    )

                ),


                float(

                    trade.get(

                        "tp",

                        0

                    )

                ),


                float(

                    trade.get(

                        "sl",

                        0

                    )

                ),


                trade.get(

                    "result",

                    ""

                )

            )

            )


            self.conn.commit()



            print(

                "[TRADE SAVED]"

            )




        except Exception as e:


            print(

                "[DB TRADE ERROR]",

                e

            )









    # =====================================================
    # LOG SAVE
    # =====================================================


    def save_log(
        self,
        message
    ):


        try:


            self.cursor.execute(

            """

            INSERT INTO logs

            VALUES(NULL,?,?)

            """,

            (

                time.strftime(

                    "%Y-%m-%d %H:%M:%S"

                ),

                str(message)

            )

            )



            self.conn.commit()



        except:


            pass







    # =====================================================
    # CLOSE
    # =====================================================


    def close(self):


        try:


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
