# =====================================================
# app.py
# Trading Application Controller
# =====================================================

import time
import threading





from api.bybit_api import bybit_api


from strategy.vwap_supertrend_strategy import (
    vwap_supertrend_strategy
)


from execution.order_manager import (
    order_manager
)


from portfolio.position_manager import (
    position_manager
)


from services.private_ws import (
    private_ws
)


from services.watchdog import (
    watchdog
)


from database.database import (
    database
)


from web.server import (
    update_status,
    add_log,
    get_trading_mode
)









class TradingApp:


    def __init__(self):


        self.running = False


        self.thread = None



        print(

            "[TRADING APP READY]"

        )









    # =====================================================
    # START
    # =====================================================

    def start(self):


        if self.running:


            return





        print("====================")

        print("[BOT START]")

        print("====================")





        self.running = True





        add_log(

            "BOT START"

        )



        update_status({


            "bot":

                "STARTING"

        })









        # -------------------------------
        # Balance Check
        # -------------------------------


        try:


            balance = (

                bybit_api

                .get_balance()

            )



            if balance:


                print(

                    "[BALANCE OK]"

                )



            else:


                print(

                    "[BALANCE SKIP]"

                )



        except Exception as e:


            print(

                "[BALANCE WARNING]",

                e

            )









        # -------------------------------
        # Private WS
        # -------------------------------


        try:


            private_ws.start()



        except Exception as e:


            print(

                "[PRIVATE WS ERROR]",

                e

            )









        # -------------------------------
        # Watchdog
        # -------------------------------


        try:


            watchdog.start()



        except Exception as e:


            print(

                "[WATCHDOG ERROR]",

                e

            )









        # -------------------------------
        # Position Sync
        # -------------------------------


        try:


            position_manager.sync()



        except Exception as e:


            print(

                "[POSITION SYNC ERROR]",

                e

            )









        # -------------------------------
        # Market Loop
        # -------------------------------


        self.thread = threading.Thread(


            target=self.market_loop,


            daemon=True


        )


        self.thread.start()









        update_status({


            "bot":

                "RUNNING"


        })



        print(

            "[BOT READY]"

        )









    # =====================================================
    # MARKET LOOP
    # =====================================================

    def market_loop(self):


        print(

            "[MARKET LOOP START]"

        )



        while self.running:



            try:



                watchdog.heartbeat()









                candles = (

                    bybit_api

                    .get_kline()

                )







                if candles:




                    formatted = []



                    for c in candles:


                        formatted.append({


                            "time":

                                int(c[0])//1000,


                            "open":

                                float(c[1]),


                            "high":

                                float(c[2]),


                            "low":

                                float(c[3]),


                            "close":

                                float(c[4]),


                            "volume":

                                float(c[5])


                        })








                    signal = (

                        vwap_supertrend_strategy

                        .analyze(

                            formatted

                        )

                    )








                    last = formatted[-1]



                    update_status({


                        "price":

                            last["close"],


                        "signal":

                            signal["signal"]

                            if signal

                            else "-"


                    })








                    if signal:



                        print(

                            "[SIGNAL]",

                            signal

                        )



                        order_manager.execute(

                            signal

                        )







                time.sleep(5)









            except Exception as e:


                print(

                    "[MARKET ERROR]",

                    e

                )


                add_log(

                    f"MARKET ERROR {e}"

                )


                time.sleep(5)









    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        print(

            "[BOT STOP]"

        )



        self.running = False





        try:


            private_ws.stop()



        except:


            pass





        try:


            watchdog.stop()



        except:


            pass





        try:


            database.close()



        except:


            pass





        update_status({


            "bot":

                "STOPPED"


        })



        add_log(

            "BOT STOPPED"

        )



        print(

            "[BOT STOP COMPLETE]"

        )









# =====================================================
# INSTANCE
# =====================================================


app = TradingApp()
