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



        # BALANCE

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





        # PRIVATE WS

        try:

            private_ws.start()


        except Exception as e:

            add_log(
                f"PRIVATE WS ERROR {e}"
            )





        # POSITION SYNC

        try:

            position_manager.refresh()


        except Exception as e:

            add_log(
                f"POSITION SYNC ERROR {e}"
            )





        # WATCHDOG

        try:

            from services.watchdog import watchdog

            watchdog.start()


        except Exception as e:

            add_log(
                f"WATCHDOG ERROR {e}"
            )





        # MARKET LOOP


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

                    interval=config.CANDLE_INTERVAL,

                    limit=config.MAX_HISTORY

                )



                if df is None:


                    time.sleep(30)

                    continue





                signal = strategy.generate_signal(

                    df

                )




                # STATUS UPDATE

                try:

                    price = market_data.price()


                    update_status({

                        "price":
                        price

                    })


                except:

                    pass






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





                    # 현재 포지션 없음

                    if size <= 0:



                        result = order_manager.open_position(

                            signal,

                            config.MAX_POSITION_SIZE

                        )


                        if result:

                            add_log(
                                f"ORDER SUCCESS {signal}"
                            )



                    # 같은 방향

                    elif side == signal:


                        add_log(

                            "EXIST POSITION SKIP"

                        )



                    # 반대 방향

                    else:


                        add_log(

                            "REVERSAL SIGNAL"

                        )


                        order_manager.close_position()


                        time.sleep(2)



                        order_manager.open_position(

                            signal,

                            config.MAX_POSITION_SIZE

                        )







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



            self.running=False




            # WS

            try:

                private_ws.stop()


            except Exception as e:

                add_log(
                    f"WS STOP ERROR {e}"
                )





            # WATCHDOG

            try:

                from services.watchdog import watchdog

                watchdog.stop()


            except:

                pass





            # THREAD

            if self.market_thread:


                if self.market_thread.is_alive():

                    self.market_thread.join(

                        timeout=5

                    )


            self.market_thread=None





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
