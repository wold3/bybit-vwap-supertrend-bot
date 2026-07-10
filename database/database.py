# database/database.py


import sqlite3
import os
import time
import threading


from config import DATABASE_PATH





class Database:


    def __init__(self):


        self.lock = threading.Lock()


        self.path = DATABASE_PATH


        self.create_folder()


        self.init_db()



        print(
            "[DATABASE READY]"
        )





    # =====================================
    # CREATE FOLDER
    # =====================================

    def create_folder(self):


        folder = os.path.dirname(
            self.path
        )


        if folder:

            os.makedirs(
                folder,
                exist_ok=True
            )







    # =====================================
    # CONNECTION
    # =====================================

    def connect(self):


        return sqlite3.connect(
            self.path
        )







    # =====================================
    # INIT TABLE
    # =====================================

    def init_db(self):


        with self.lock:


            conn = self.connect()


            cur = conn.cursor()



            # ORDERS

            cur.execute(
            """

            CREATE TABLE IF NOT EXISTS orders(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                order_id TEXT,

                symbol TEXT,

                side TEXT,

                qty REAL,

                price REAL,

                status TEXT,

                timestamp INTEGER

            )

            """
            )





            # EXECUTIONS

            cur.execute(
            """

            CREATE TABLE IF NOT EXISTS executions(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                exec_id TEXT,

                order_id TEXT,

                symbol TEXT,

                side TEXT,

                qty REAL,

                price REAL,

                timestamp INTEGER

            )

            """
            )







            # POSITIONS

            cur.execute(
            """

            CREATE TABLE IF NOT EXISTS positions(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                symbol TEXT,

                side TEXT,

                size REAL,

                entry_price REAL,

                pnl REAL,

                timestamp INTEGER

            )

            """
            )








            # SIGNALS

            cur.execute(
            """

            CREATE TABLE IF NOT EXISTS signals(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                type TEXT,

                side TEXT,

                price REAL,

                vwap REAL,

                supertrend INTEGER,

                timestamp INTEGER

            )

            """
            )







            # ERRORS

            cur.execute(
            """

            CREATE TABLE IF NOT EXISTS errors(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                message TEXT,

                timestamp INTEGER

            )

            """
            )







            # SYSTEM EVENTS

            cur.execute(
            """

            CREATE TABLE IF NOT EXISTS system_events(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                event TEXT,

                timestamp INTEGER

            )

            """
            )





            conn.commit()


            conn.close()







    # =====================================
    # SAVE ORDER
    # =====================================

    def save_order(
        self,
        order
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
                price,
                status,
                timestamp

                )

                VALUES (?,?,?,?,?,?,?)

                """,

                (

                order.get(
                    "orderId"
                ),

                order.get(
                    "symbol"
                ),

                order.get(
                    "side"
                ),

                float(
                    order.get(
                        "qty",
                        0
                    )
                ),

                0,

                order.get(
                    "orderStatus"
                ),

                int(
                    time.time()
                )

                )

                )



                conn.commit()

                conn.close()



        except Exception as e:


            self.save_error(
                str(e)
            )







    # =====================================
    # SAVE POSITION
    # =====================================

    def save_position(
        self,
        position
    ):


        with self.lock:


            conn = self.connect()


            cur = conn.cursor()



            cur.execute(
            """

            INSERT INTO positions

            (

            symbol,
            side,
            size,
            entry_price,
            pnl,
            timestamp

            )

            VALUES(?,?,?,?,?,?)

            """,

            (

            position.get(
                "symbol"
            ),

            position.get(
                "side"
            ),

            position.get(
                "size"
            ),

            position.get(
                "entry_price"
            ),

            position.get(
                "unrealized_pnl"
            ),

            int(
                time.time()
            )

            )

            )


            conn.commit()


            conn.close()







    # =====================================
    # SAVE SIGNAL
    # =====================================

    def save_signal(
        self,
        signal
    ):


        with self.lock:


            conn = self.connect()


            cur = conn.cursor()



            cur.execute(
            """

            INSERT INTO signals

            (

            type,
            side,
            price,
            vwap,
            supertrend,
            timestamp

            )

            VALUES(?,?,?,?,?,?)

            """,

            (

            signal.get(
                "type"
            ),

            signal.get(
                "side"
            ),

            signal.get(
                "price"
            ),

            signal.get(
                "vwap"
            ),

            signal.get(
                "supertrend"
            ),

            int(
                time.time()
            )

            )

            )


            conn.commit()


            conn.close()







    # =====================================
    # SAVE ERROR
    # =====================================

    def save_error(
        self,
        message
    ):


        try:


            conn = self.connect()


            cur = conn.cursor()



            cur.execute(
            """

            INSERT INTO errors

            (

            message,
            timestamp

            )

            VALUES(?,?)

            """,

            (

            message,

            int(
                time.time()
            )

            )

            )


            conn.commit()


            conn.close()



        except:


            pass







    # =====================================
    # EVENT
    # =====================================

    def event(
        self,
        message
    ):


        with self.lock:


            conn = self.connect()


            cur = conn.cursor()



            cur.execute(
            """

            INSERT INTO system_events

            (

            event,
            timestamp

            )

            VALUES(?,?)

            """,

            (

            message,

            int(
                time.time()
            )

            )

            )


            conn.commit()


            conn.close()





database = Database()
