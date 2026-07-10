# =====================================================
# app.py
# Trading Application Core
# =====================================================

import time
import threading



from config import (
    DEFAULT_SYMBOL
)



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


from risk.risk_manager import (
    risk_manager
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



# ============================
# WEB DASHBOARD
# ============================

from web.server import (
    start_dashboard,
    update_status
)





class TradingApp:



    def __init__(self):


        self.running = False


        self.market_thread = None


        print(

            "[TRADING APP READY]"

        )







    # =====================================================
    # START
    # =====================================================

    def start(self):


        try:


            print("====================")

            print("[BOT START]")

            print("====================")



            # WEB

            start_dashboard()






            # WALLET


            wallet = (

                bybit_api

                .get_wallet_balance()

            )



            if not wallet:


                raise Exception(

                    "WALLET ERROR"

                )





            equity = float(

                wallet

                ["result"]

                ["list"][0]

                ["totalEquity"]

            )



            print(

                "[EQUITY]",

                equity

            )



            risk_manager.update_equity(

                equity

            )






            # POSITION


            try:


                position_manager.sync()



            except Exception:


                print(

                    "[POSITION SYNC ERROR]"

                )






            # STATUS


            update_status(

                {


                "bot":

                    "STARTING",


                "symbol":

                    DEFAULT_SYMBOL


                }

            )






            # SERVICES


            print(

                "[PRIVATE WS CONNECTING]"

            )


            private_ws.start()



            watchdog.start()







            self.running = True





            self.market_thread = threading.Thread(

                target=self.market_loop,

                daemon=True

            )



            self.market_thread.start()






            update_status(

                {


                "bot":

                    "RUNNING"


                }

            )




            print(

                "[BOT READY]"

            )







        except Exception as e:



            print(

                "[START ERROR]",

                e

            )


            self.stop()


            raise e










    # =====================================================
    # MARKET LOOP
    # =====================================================

    def market_loop(self):


        print(

            "[MARKET THREAD START]"

        )



        while self.running:



            try:



                candles = (

                    bybit_api

                    .get_kline()

                )





                if candles:



                    print(

                        "[KLINE]",

                        len(candles)

                    )





                    data = []



                    for c in candles:


                        data.append(

                            {


                            "timestamp":

                                c[0],


                            "open":

                                c[1],


                            "high":

                                c[2],


                            "low":

                                c[3],


                            "close":

                                c[4],


                            "volume":

                                c[5]


                            }

                        )





                    print(

                        "[CANDLE RECEIVED]",

                        len(data)

                    )






                    signal = (

                        vwap_supertrend_strategy

                        .analyze(

                            data

                        )

                    )






                    # ==========================
                    # DASHBOARD UPDATE
                    # ==========================


                    last = data[-1]



                    update_status(

                        {


                        "price":

                            float(last["close"]),



                        }

                    )








                    if signal:


                        print(

                            "[APP SIGNAL]",

                            signal

                        )


                        order_manager.execute(

                            signal

                        )






                    else:


                        print(

                            "[NO SIGNAL]"

                        )







                watchdog.heartbeat()





            except Exception as e:



                print(

                    "[MARKET LOOP ERROR]",

                    e

                )


                database.save_error(

                    e

                )





            time.sleep(

                10

            )











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





        update_status(

            {


            "bot":

                "STOPPED"


            }

        )



        print(

            "[BOT STOP COMPLETE]"

        )









# =====================================================
# SINGLETON
# =====================================================


app = TradingApp()
