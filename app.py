# app.py


import time
import threading



from api.bybit_api import bybit_api


from risk.risk_manager import risk_manager


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


from services.telegram_bot import (
    telegram_bot
)


from database.database import (
    database
)







class TradingApp:



    def __init__(self):


        self.running = False


        self.market_thread = None







    # =====================================
    # START
    # =====================================

    def start(self):


        print("====================")
        print("[BOT START]")
        print("====================")



        try:


            if not bybit_api.ping():


                raise Exception(
                    "BYBIT CONNECTION FAILED"
                )





            wallet = (

                bybit_api
                .get_wallet_balance()

            )



            if wallet is None:


                raise Exception(
                    "WALLET ERROR"
                )





            equity = (

                self.parse_equity(

                    wallet

                )

            )



            print(
                "[EQUITY]",
                equity
            )





            position_manager.sync()





            risk_manager.initialize(

                equity

            )





            bybit_api.set_leverage()





            database.event(

                "BOT START"

            )





            telegram_bot.bot_start()





            #
            # 중요:
            # thread 시작 전에 running True
            #

            self.running = True





            private_ws.start()


            watchdog.start()





            self.start_market_stream()





            print(
                "[BOT READY]"
            )





        except Exception as e:


            print(
                "[START ERROR]",
                e
            )


            database.save_error(

                str(e)

            )



            telegram_bot.error(

                str(e)

            )


            self.stop()


            raise e







    # =====================================
    # MARKET LOOP
    # =====================================

    def start_market_stream(self):


        print(
            "[MARKET THREAD START]"
        )



        def run():


            while self.running:


                try:


                    candles = (

                        bybit_api
                        .get_kline()

                    )



                    if candles:


                        print(

                            "[CANDLE RECEIVED]",

                            len(candles)

                        )


                        self.on_candle(

                            candles

                        )



                    watchdog.heartbeat()



                except Exception as e:


                    print(

                        "[MARKET ERROR]",

                        e

                    )


                    database.save_error(

                        str(e)

                    )





                time.sleep(60)







        self.market_thread = threading.Thread(

            target=run,

            daemon=True

        )



        self.market_thread.start()







    # =====================================
    # CANDLE PROCESS
    # =====================================

    def on_candle(

        self,

        candles

    ):


        if not self.running:


            return





        try:


            signal = (

                vwap_supertrend_strategy
                .analyze(

                    candles

                )

            )



        except Exception as e:


            print(

                "[STRATEGY ERROR]",

                e

            )


            database.save_error(

                str(e)

            )


            return





        if signal is None:


            print(

                "[NO SIGNAL]"

            )


            return





        print(

            "[SIGNAL]",

            signal

        )





        database.save_signal(

            signal

        )







        # EXIT

        if signal.get(

            "type"

        ) == "EXIT":



            order_manager.close_position()



            return







        # ENTRY RISK CHECK


        if not risk_manager.can_trade():



            print(

                "[RISK BLOCK]"

            )


            return







        order_manager.execute(

            signal

        )











    # =====================================
    # EQUITY PARSE
    # =====================================

    def parse_equity(

        self,

        wallet

    ):



        try:


            return float(

                wallet

                ["result"]

                ["list"][0]

                ["totalEquity"]

            )



        except Exception as e:



            print(

                "[EQUITY PARSE ERROR]",

                e

            )


            return 0







    # =====================================
    # STOP
    # =====================================

    def stop(self):


        print(

            "[BOT STOP]"

        )



        self.running = False





        try:



            database.event(

                "BOT STOP"

            )



            telegram_bot.bot_stop()



            private_ws.stop()



            watchdog.stop()



        except Exception as e:



            print(

                "[STOP ERROR]",

                e

            )



            database.save_error(

                str(e)

            )





        print(

            "[BOT STOP COMPLETE]"

        )
