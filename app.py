# =======================================================
# app.py
# VWAP SuperTrend Trading Bot Core
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





        # -------------------------------------------------
        # BALANCE CHECK
        # -------------------------------------------------

        try:


            balance = bybit_api.get_balance()



            if balance:


                print(

                    "[BALANCE OK]"

                )


            else:


                print(

                    "[BALANCE CHECK FAILED - CONTINUE]"

                )



        except Exception as e:


            print(

                "[BALANCE ERROR PROTECTED]",

                e

            )





        # -------------------------------------------------
        # PRIVATE WS
        # -------------------------------------------------

        try:


            private_ws.start()



            print(

                "[PRIVATE WS STARTED]"

            )


        except Exception as e:


            print(

                "[PRIVATE WS ERROR]",

                e

            )





        # -------------------------------------------------
        # POSITION SYNC
        # -------------------------------------------------

        try:


            position_manager.refresh()



        except Exception as e:


            print(

                "[POSITION SYNC ERROR]",

                e

            )





        # -------------------------------------------------
        # WATCHDOG
        # -------------------------------------------------

        try:


            from services.watchdog import watchdog


            watchdog.start()



            print(

                "[WATCHDOG START]"

            )



        except Exception:


            pass





        # -------------------------------------------------
        # MARKET LOOP
        # -------------------------------------------------

        if (

            self.market_thread is None

            or

            not self.market_thread.is_alive()

        ):



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





    # =====================================================
    # MARKET LOOP
    # =====================================================

    def market_loop(self):


        from market.market_data import market_data

        from strategy.vwap_supertrend import strategy



        print(

            "[MARKET LOOP START]"

        )



        while self.running:



            try:



                df = market_data.get_candles(

                    interval="5",

                    limit=200

                )



                if df is None:



                    time.sleep(30)

                    continue





                signal = strategy.generate_signal(

                    df

                )





                if signal:



                    print(

                        "[SIGNAL]",

                        signal

                    )


                    add_log(

                        f"SIGNAL {signal}"

                    )





                    position = position_manager.get_position()



                    current = position.get(

                        "side",

                        "NONE"

                    )



                    size = position.get(

                        "size",

                        0

                    )





                    # ---------------------------------
                    # EXIST POSITION PROTECTION
                    # ---------------------------------

                    if size > 0:



                        if current == signal:



                            add_log(

                                "SKIP EXIST POSITION"

                            )

                            time.sleep(30)

                            continue




                        else:



                            add_log(

                                "DIFFERENT POSITION EXISTS"

                            )


                            time.sleep(30)

                            continue





                    # ---------------------------------
                    # ORDER
                    # ---------------------------------

                    qty = config.MAX_POSITION_SIZE



                    result = order_manager.open_position(

                        signal,

                        qty

                    )



                    if result:



                        add_log(

                            f"ORDER SUCCESS {signal}"

                        )


                    else:


                        add_log(

                            "ORDER FAILED"

                        )





                # candle 보호

                time.sleep(30)





            except Exception as e:



                traceback.print_exc()



                add_log(

                    f"MARKET LOOP ERROR {e}"

                )



                time.sleep(10)





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





            # -------------------------------------------------
            # CLOSE POSITION
            # -------------------------------------------------

            try:


                order_manager.close_position()



            except Exception as e:


                print(

                    "[POSITION CLOSE ERROR]",

                    e

                )





            # -------------------------------------------------
            # PRIVATE WS
            # -------------------------------------------------

            try:


                private_ws.stop()



            except Exception as e:


                print(

                    "[WS STOP ERROR]",

                    e

                )





            # -------------------------------------------------
            # WATCHDOG
            # -------------------------------------------------

            try:


                from services.watchdog import watchdog


                watchdog.stop()



            except Exception:


                pass





            # -------------------------------------------------
            # THREAD JOIN
            # -------------------------------------------------

            if (

                self.market_thread

                and

                self.market_thread.is_alive()

            ):


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

                "[BOT STOP COMPLETE]"

            )





# =======================================================
# NO GLOBAL INSTANCE
# main.py에서 생성
# =======================================================
