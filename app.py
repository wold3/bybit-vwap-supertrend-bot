# =====================================================
# app.py
# Trading Application Core
# =====================================================

import time
import threading


from config import DEFAULT_SYMBOL


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


from web.server import (
    start_dashboard,
    update_status,
    add_log
)


from web.chart_data import (
    add_candle
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



            start_dashboard()



            update_status({

                "bot":
                    "STARTING",

                "symbol":
                    DEFAULT_SYMBOL

            })





            # =========================
            # WALLET
            # =========================


            wallet = bybit_api.get_wallet_balance()



            if not wallet:

                raise Exception(
                    "WALLET ERROR"
                )



            if wallet.get("retCode") != 0:

                raise Exception(

                    wallet.get(

                        "retMsg",

                        "WALLET ERROR"

                    )

                )





            try:


                equity = float(

                    wallet["result"]
                    ["list"][0]
                    ["totalEquity"]

                )


            except Exception:


                raise Exception(
                    "WALLET DATA ERROR"
                )





            print(
                "[EQUITY]",
                equity
            )


            add_log(

                f"EQUITY {equity}"

            )


            risk_manager.update_equity(

                equity

            )







            # =========================
            # POSITION SYNC
            # =========================


            try:


                position_manager.sync()


                print(

                    "[POSITION SYNC OK]"

                )


            except Exception as e:


                print(

                    "[POSITION SYNC ERROR]",

                    e

                )









            # =========================
            # WATCHDOG
            # =========================


            watchdog.start()


            print(

                "[WATCHDOG START]"

            )







            # =========================
            # PRIVATE WS
            # =========================


            print(

                "[PRIVATE WS CONNECTING]"

            )


            private_ws.start()







            # =========================
            # MARKET THREAD
            # =========================


            self.running = True



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







        except Exception as e:


            print(

                "[START ERROR]",

                e

            )



            try:

                database.save_error(e)

            except:

                pass



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



                candles = bybit_api.get_kline()



                if candles:



                    print(

                        "[KLINE]",

                        len(candles)

                    )



                    data = []



                    for c in candles:


                        data.append({

                            "timestamp":

                                int(c[0]),


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





                    print(

                        "[CANDLE RECEIVED]",

                        len(data)

                    )





                    last = data[-1]







                    add_candle({

                        "time":

                            last["timestamp"],


                        "open":

                            last["open"],


                        "high":

                            last["high"],


                        "low":

                            last["low"],


                        "close":

                            last["close"]

                    })









                    signal = (

                        vwap_supertrend_strategy

                        .analyze(

                            data

                        )

                    )







                    indicator = getattr(

                        vwap_supertrend_strategy,

                        "last_indicator",

                        {}

                    )





                    update_status({

                        "price":

                            last["close"],


                        "vwap":

                            indicator.get(

                                "vwap",

                                0

                            ),


                        "trend":

                            indicator.get(

                                "trend",

                                "NONE"

                            ),


                        "volume":

                            indicator.get(

                                "volume",

                                False

                            )

                    })









                    if signal:



                        print(

                            "[SIGNAL]",

                            signal

                        )


                        add_log(

                            str(signal)

                        )



                        result = (

                            order_manager.execute(

                                signal,

                                last["close"]

                            )

                        )



                        if result:


                            print(

                                "[ORDER RESULT]",

                                result

                            )


                            add_log(

                                str(result)

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


                try:

                    database.save_error(e)

                except:

                    pass



                try:

                    add_log(str(e))

                except:

                    pass






            time.sleep(10)









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





        try:


            update_status({

                "bot":

                    "STOPPED"

            })


            add_log(

                "BOT STOPPED"

            )


        except:

            pass





        print(

            "[BOT STOP COMPLETE]"

        )








# =====================================================
# INSTANCE
# =====================================================


app = TradingApp()
