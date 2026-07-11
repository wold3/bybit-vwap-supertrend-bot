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


        self.conn = None

        self.cursor = None


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


        self.cursor = self.conn.cursor()







    # =====================================================
    # CHECK CONNECTION
    # =====================================================


    def ensure_connection(self):


        try:


            self.cursor.execute(
                "SELECT 1"
            )


        except:


            self.connect()







    # =====================================================
    # CREATE TABLE
    # =====================================================


    def create_tables(self):


        self.ensure_connection()



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


            result TEXT,


            pnl REAL DEFAULT 0


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


            self.ensure_connection()



            self.cursor.execute(

            """

            INSERT INTO errors

            (

            time,

            error

            )

            VALUES (?,?)

            """,

            (

                self.now(),

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


            self.ensure_connection()



            self.cursor.execute(

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

            result,

            pnl

            )

            VALUES (?,?,?,?,?,?,?,?,?)

            """,

            (

                self.now(),


                trade.get(
                    "symbol",
                    "BTCUSDT"
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
                    "OPEN"
                ),


                float(
                    trade.get(
                        "pnl",
                        0
                    )
                )


            )

            )



            self.conn.commit()



            print(

                "[TRADE SAVED]"

            )



        except Exception as e:


            print(

                "[TRADE SAVE ERROR]",

                e

            )








    # =====================================================
    # UPDATE TRADE RESULT
    # =====================================================


    def update_trade_result(
        self,
        trade_id,
        result,
        pnl
    ):


        try:


            self.ensure_connection()



            self.cursor.execute(

            """

            UPDATE trades

            SET

            result=?,

            pnl=?

            WHERE id=?

            """,

            (

                result,

                pnl,

                trade_id

            )

            )



            self.conn.commit()



        except Exception as e:


            print(

                "[TRADE UPDATE ERROR]",

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


            self.ensure_connection()



            self.cursor.execute(

            """

            INSERT INTO logs

            (

            time,

            message

            )

            VALUES (?,?)

            """,

            (

                self.now(),

                str(message)

            )

            )



            self.conn.commit()



        except:


            pass







    # =====================================================
    # TRADE STATISTICS
    # =====================================================


    def get_trade_stats(self):


        try:


            self.ensure_connection()



            self.cursor.execute(

            """

            SELECT COUNT(*)

            FROM trades

            """

            )


            total = (

                self.cursor

                .fetchone()[0]

            )



            self.cursor.execute(

            """

            SELECT COUNT(*)

            FROM trades

            WHERE result='WIN'

            """

            )


            win = (

                self.cursor

                .fetchone()[0]

            )



            self.cursor.execute(

            """

            SELECT COUNT(*)

            FROM trades

            WHERE result='LOSS'

            """

            )


            loss = (

                self.cursor

                .fetchone()[0]

            )



            self.cursor.execute(

            """

            SELECT SUM(pnl)

            FROM trades

            """

            )


            pnl = (

                self.cursor

                .fetchone()[0]

            )



            if pnl is None:

                pnl = 0





            winrate = 0



            if total > 0:


                winrate = (

                    win /

                    total *

                    100

                )





            return {


                "total":

                    total,


                "win":

                    win,


                "loss":

                    loss,


                "winrate":

                    round(
                        winrate,
                        2
                    ),


                "pnl":

                    round(
                        pnl,
                        4
                    )

            }





        except Exception as e:


            print(

                "[STAT ERROR]",

                e

            )


            return {}









    # =====================================================
    # RECENT TRADES
    # =====================================================


    def get_recent_trades(
        self,
        limit=20
    ):


        try:


            self.ensure_connection()



            self.cursor.execute(

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


            return (

                self.cursor

                .fetchall()

            )



        except:


            return []









    # =====================================================
    # TIME
    # =====================================================


    def now(self):


        return time.strftime(

            "%Y-%m-%d %H:%M:%S"

        )









    # =====================================================
    # CLOSE
    # =====================================================


    def close(self):


        try:


            if self.conn:


                self.conn.close()



                self.conn = None


                self.cursor = None



                print(

                    "[DATABASE CLOSED]"

                )



        except Exception as e:


            print(

                "[DB CLOSE ERROR]",

                e

            )









# =====================================================
# INSTANCE
# =====================================================


database = Database()
