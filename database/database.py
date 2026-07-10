# database/database.py


import sqlite3
import threading
import time


from config import DATABASE_PATH




class Database:



    def __init__(self):


        self.path = DATABASE_PATH


        self.lock = threading.Lock()


        self.init_db()



    # =====================================
    # INIT DATABASE
    # =====================================

    def init_db(self):


        with self.lock:


            conn = sqlite3.connect(

                self.path

            )


            cursor = conn.cursor()



            # Trades

            cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS trades (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    symbol TEXT,

                    side TEXT,

                    entry REAL,

                    exit REAL,

                    qty REAL,

                    pnl REAL,

                    timestamp INTEGER

                )

                """
            )




            # Orders

            cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS orders (

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





            # Signals

            cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS signals (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    signal_type TEXT,

                    side TEXT,

                    price REAL,

                    timestamp INTEGER

                )

                """
            )






            # Equity

            cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS equity (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    value REAL,

                    timestamp INTEGER

                )

                """
            )






            # Errors

            cursor.execute(
                """

                CREATE TABLE IF NOT EXISTS errors (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    message TEXT,

                    timestamp INTEGER

                )

                """
            )



            conn.commit()


            conn.close()



        print(

            "[DATABASE READY]"

        )





    # =====================================
    # INSERT SIGNAL
    # =====================================

    def save_signal(
        self,
        signal
    ):


        self.execute(

            """

            INSERT INTO signals

            (

            signal_type,

            side,

            price,

            timestamp

            )

            VALUES (?,?,?,?)

            """,

            (

                signal["type"],

                signal.get("side"),

                signal.get("price"),

                int(time.time())

            )

        )






    # =====================================
    # SAVE ORDER
    # =====================================

    def save_order(
        self,
        order
    ):


        self.execute(

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

                order.get("orderId"),

                order.get("symbol"),

                order.get("side"),

                float(

                    order.get(

                        "qty",

                        0

                    )

                ),

                float(

                    order.get(

                        "price",

                        0

                    )

                ),

                order.get(

                    "orderStatus"

                ),

                int(time.time())

            )

        )






    # =====================================
    # SAVE TRADE
    # =====================================

    def save_trade(
        self,
        data
    ):


        self.execute(

            """

            INSERT INTO trades

            (

            symbol,

            side,

            entry,

            exit,

            qty,

            pnl,

            timestamp

            )

            VALUES (?,?,?,?,?,?,?)

            """,

            (

                data["symbol"],

                data["side"],

                data["entry"],

                data["exit"],

                data["qty"],

                data["pnl"],

                int(time.time())

            )

        )






    # =====================================
    # EQUITY
    # =====================================

    def save_equity(
        self,
        equity
    ):


        self.execute(

            """

            INSERT INTO equity

            (

            value,

            timestamp

            )

            VALUES (?,?)

            """,

            (

                equity,

                int(time.time())

            )

        )







    # =====================================
    # ERROR
    # =====================================

    def save_error(
        self,
        error
    ):


        self.execute(

            """

            INSERT INTO errors

            (

            message,

            timestamp

            )

            VALUES (?,?)

            """,

            (

                str(error),

                int(time.time())

            )

        )






    # =====================================
    # EXECUTE
    # =====================================

    def execute(
        self,
        query,
        params
    ):


        try:


            with self.lock:


                conn = sqlite3.connect(

                    self.path

                )


                cursor = conn.cursor()


                cursor.execute(

                    query,

                    params

                )


                conn.commit()


                conn.close()



        except Exception as e:


            print(

                "[DB ERROR]",

                e

            )







database = Database()
