# =====================================================
# app.py
# VWAP SUPERTREND BOT APPLICATION
# =====================================================

import time
import threading





from api.bybit_api import (
    bybit_api
)


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
    add_log
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






        # Private WS

        private_ws.start()





        # Watchdog

        watchdog.start()







        # Position Sync

        position_manager.sync()








        # Market Thread


        self.thread = threading.Thread(

            target=self.market_loop,

            daemon=True

        )


        self.thread.start()







        add_log(

            "BOT START"

        )



        update_status({

            "bot":

                "RUNNING"

        })









    # =====================================================
    # MARKET LOOP
    # =====================================================


    def market_loop(self):


        print(

            "[MARKET THREAD START]"

        )



        while self.running:


            try:



                watchdog.heartbeat()





                candles = (

                    bybit_api

                    .get_kline()

                )





                if candles:





                    # Bybit candle 변환


                    formatted = []



                    for c in candles:


                        formatted.append({


                            "time":

                                int(c[0]) // 1000,


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






                    indicator = (

                        vwap_supertrend_strategy

                        .last_indicator

                    )





                    update_status({


                        "price":

                            formatted[-1]["close"],


                        "vwap":

                            indicator.get(

                                "vwap",

                                0

                            ),


                        "trend":

                            indicator.get(

                                "trend",

                                "-"

                            )

                    })








                    if signal:


                        print(

                            "[SIGNAL]",

                            signal

                        )



                        update_status({

                            "signal":

                                signal["signal"]

                        })



                        order_manager.execute(

                            signal

                        )






                time.sleep(5)






            except Exception as e:



                print(

                    "[MARKET LOOP ERROR]",

                    e

                )


                database.save_error(

                    e

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





        private_ws.stop()


        watchdog.stop()





        database.close()





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
