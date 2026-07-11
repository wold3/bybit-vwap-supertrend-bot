# =======================================================
# app.py
# VWAP SUPERTREND AUTO BOT CORE
# =======================================================

import time
import threading
import traceback


import config


from api.bybit_api import bybit_api

from services.private_ws import private_ws

from portfolio.position_manager import position_manager

from order.order_manager import order_manager


from web.server import (

    update_status,

    add_log

)





class TradingApp:


    def __init__(self):


        self.running = False

        self.market_thread = None

        self.lock = threading.Lock()



        print(

            "[TRADING APP READY]"

        )





    # ===================================================
    # START
    # ===================================================

    def start(self):


        with self.lock:


            if self.running:

                return


            self.running = True



        print()

        print("====================")

        print("[BOT START]")

        print("====================")





        # -----------------------------
        # BALANCE
        # -----------------------------

        try:


            balance = bybit_api.get_balance()



            if balance:


                print(

                    "[BALANCE OK]"

                )

            else:


                print(

                    "[BALANCE CHECK FAILED]"

                )



        except Exception as e:


            add_log(

                f"BALANCE ERROR {e}"

            )







        # -----------------------------
        # PRIVATE WS
        # -----------------------------

        try:


            private_ws.start()


            print(

                "[PRIVATE WS STARTED]"

            )


        except Exception as e:


            add_log(

                f"PRIVATE WS ERROR {e}"

            )







        # -----------------------------
        # POSITION SYNC
        # -----------------------------

        try:


            position_manager.refresh()



        except Exception as e:


            add_log(

                f"POSITION SYNC ERROR {e}"

            )








        # -----------------------------
        # WATCHDOG
        # -----------------------------

        try:


            from services.watchdog import watchdog


            watchdog.start()



            print(

                "[WATCHDOG START]"

            )


        except Exception as e:


            add_log(

                f"WATCHDOG ERROR {e}"

            )









        # -----------------------------
        # MARKET THREAD
        # -----------------------------

        self.market_thread = threading.Thread(


            target=self.market_loop,


            daemon=True,


            name="MarketLoop"


        )


        self.market_thread.start()






        update_status({

            "bot":

            "RUNNING"

        })



        add_log(

            "BOT START"

        )



        print(

            "[BOT READY]"

        )









    # ===================================================
    # MARKET LOOP
    # ===================================================

    def market_loop(self):


        from market.market_data import market_data


        from strategy.vwap_supertrend import strategy





        print(

            "[MARKET LOOP START]"

        )





        while self.running:



            try:




                df = market_data.get_candles(


                    interval=str(

                        config.CANDLE_INTERVAL

                    ),


                    limit=config.MAX_HISTORY


                )




                if df is None:


                    time.sleep(10)

                    continue





                signal = strategy.generate_signal(

                    df

                )






                if signal:



                    add_log(

                        f"SIGNAL {signal}"

                    )



                    position = position_manager.get_position()



                    side = position.get(

                        "side",

                        "NONE"

                    )


                    size = float(

                        position.get(

                            "size",

                            0

                        )

                    )







                    if size > 0:



                        if side == signal:


                            add_log(

                                "SAME POSITION SKIP"

                            )


                        else:


                            add_log(

                                "OPPOSITE POSITION EXISTS"

                            )



                        time.sleep(30)

                        continue







                    result = order_manager.open_position(


                        signal,


                        config.MAX_POSITION_SIZE


                    )



                    if result:


                        add_log(

                            f"ORDER SUCCESS {signal}"

                        )


                    else:


                        add_log(

                            "ORDER FAILED"

                        )







                time.sleep(30)








            except Exception as e:



                traceback.print_exc()



                add_log(

                    f"MARKET LOOP ERROR {e}"

                )



                time.sleep(10)









    # ===================================================
    # STOP
    # ===================================================

    def stop(self):


        with self.lock:



            if not self.running:


                return



            self.running = False





        print()

        print("====================")

        print("[BOT STOP]")

        print("====================")







        # CLOSE POSITION

        try:


            order_manager.close_position()



        except Exception as e:


            add_log(

                f"CLOSE ERROR {e}"

            )







        # PRIVATE WS STOP

        try:


            private_ws.stop()



        except Exception as e:


            add_log(

                f"WS STOP ERROR {e}"

            )







        # WATCHDOG STOP

        try:


            from services.watchdog import watchdog


            watchdog.stop()



        except Exception:


            pass








        if self.market_thread:



            if self.market_thread.is_alive():


                self.market_thread.join(

                    timeout=5

                )



        self.market_thread = None






        update_status({

            "bot":

            "STOPPED"

        })



        add_log(

            "BOT STOP COMPLETE"

        )



        print(

            "[SYSTEM SHUTDOWN]"

        )





# =======================================================
# EXPORT
# =======================================================

__all__ = [

    "TradingApp"

]
