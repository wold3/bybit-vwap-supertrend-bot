# =====================================================
# app.py
# VWAP SUPERTREND AUTO BOT CORE
# =====================================================

import time
import threading


import config


from api.bybit_api import bybit_api


from services.private_ws import private_ws


from portfolio.position_manager import position_manager


from risk.risk_manager import risk_manager


from order.order_manager import order_manager


from web.server import (
    update_status,
    add_log
)






class TradingApp:


    def __init__(self):

        self.running = False

        self.market_thread = None

        self.stop_lock = threading.Lock()


        print(
            "[TRADING APP READY]"
        )





    # =====================================================
    # START
    # =====================================================

    def start(self):


        if self.running:

            return



        print()
        print("====================")
        print("[BOT START]")
        print("====================")



        self.running = True




        # -----------------------------
        # API TEST
        # -----------------------------

        try:

            balance = bybit_api.get_balance()


            if balance is not None:

                print(
                    "[BALANCE OK]"
                )

            else:

                print(
                    "[BALANCE CHECK FAILED]"
                )


        except Exception as e:

            print(
                "[BALANCE ERROR]",
                e
            )






        # -----------------------------
        # PRIVATE WS
        # -----------------------------

        try:

            private_ws.start()


        except Exception as e:

            print(
                "[PRIVATE WS ERROR]",
                e
            )







        # -----------------------------
        # WATCHDOG
        # -----------------------------

        try:


            from watchdog import watchdog


            watchdog.start()


            print(
                "[WATCHDOG START]"
            )


        except Exception:


            pass







        # -----------------------------
        # MARKET LOOP
        # -----------------------------

        self.market_thread = threading.Thread(

            target=self.market_loop,

            daemon=True

        )


        self.market_thread.start()



        update_status({

            "bot":

                "RUNNING"

        })


        add_log(

            "BOT READY"

        )



        print(
            "[BOT READY]"
        )










    # =====================================================
    # MARKET LOOP
    # =====================================================

    def market_loop(self):


        from market.market_data import (

            market_data

        )


        from strategy.vwap_supertrend import (

            strategy

        )


        print(

            "[MARKET LOOP START]"

        )



        while self.running:


            try:



                # -----------------------------
                # KLINE DATA
                # -----------------------------

                df = market_data.get_candles(

                    interval="5",

                    limit=200

                )



                if df is None:


                    time.sleep(5)

                    continue






                # -----------------------------
                # SIGNAL
                # -----------------------------

                signal = strategy.generate_signal(

                    df

                )






                if signal:



                    add_log(

                        f"SIGNAL {signal}"

                    )


                    print(

                        "[SIGNAL]",

                        signal

                    )







                    # -----------------------------
                    # POSITION CHECK
                    # -----------------------------

                    pos = (

                        position_manager

                        .get_position()

                    )



                    current = pos.get(

                        "side",

                        "NONE"

                    )






                    if (

                        signal == "Buy"

                        and

                        current == "Buy"

                    ):


                        add_log(

                            "SKIP EXIST BUY"

                        )

                        time.sleep(10)

                        continue







                    if (

                        signal == "Sell"

                        and

                        current == "Sell"

                    ):


                        add_log(

                            "SKIP EXIST SELL"

                        )

                        time.sleep(10)

                        continue







                    # -----------------------------
                    # ORDER
                    # -----------------------------

                    qty = config.MAX_POSITION_SIZE



                    result = (

                        order_manager

                        .open_position(

                            signal,

                            qty

                        )

                    )



                    if result:



                        add_log(

                            f"ORDER SUCCESS {signal}"

                        )


                    else:


                        add_log(

                            "ORDER FAILED"

                        )







                time.sleep(10)







            except Exception as e:



                add_log(

                    f"MARKET LOOP ERROR {e}"

                )


                time.sleep(5)









    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        with self.stop_lock:



            if not self.running:


                return





            print()

            print("====================")

            print("[BOT STOP]")

            print("====================")




            self.running = False







            # -----------------------------
            # PRIVATE WS
            # -----------------------------

            try:


                private_ws.stop()


            except Exception as e:


                print(

                    "[WS STOP ERROR]",

                    e

                )








            # -----------------------------
            # WATCHDOG
            # -----------------------------

            try:


                from watchdog import watchdog


                watchdog.stop()


                print(

                    "[WATCHDOG STOPPED]"

                )


            except Exception:


                pass







            # -----------------------------
            # POSITION
            # -----------------------------

            try:


                position_manager.close()


            except Exception as e:


                print(

                    "[POSITION ERROR]",

                    e

                )







            update_status({

                "bot":

                    "STOPPED"

            })


            add_log(

                "BOT STOP COMPLETE"

            )



            print(

                "[BOT STOP COMPLETE]"

            )
