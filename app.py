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

from database.database import (
    database
)


# Telegram이 아직 없을 경우 대비
try:
    from services.telegram_bot import telegram_bot
except Exception:

    class TelegramDummy:

        def bot_start(self):
            pass

        def bot_stop(self):
            pass

        def error(self, msg):
            pass


    telegram_bot = TelegramDummy()



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

            # -----------------------------
            # API CHECK
            # -----------------------------

            if not bybit_api.ping():

                raise Exception(
                    "BYBIT CONNECTION FAILED"
                )



            # -----------------------------
            # WALLET
            # -----------------------------

            wallet = (
                bybit_api
                .get_wallet_balance()
            )


            if wallet is None:

                raise Exception(
                    "WALLET ERROR"
                )



            equity = self.parse_equity(
                wallet
            )



            print(
                "[EQUITY]",
                equity
            )



            # -----------------------------
            # POSITION SYNC
            # -----------------------------

            position_manager.sync()



            # -----------------------------
            # RISK INIT
            # -----------------------------

            risk_manager.initialize(
                equity
            )



            # -----------------------------
            # LEVERAGE
            # -----------------------------

            bybit_api.set_leverage()



            # -----------------------------
            # DATABASE
            # -----------------------------

            database.event(
                "BOT START"
            )



            # -----------------------------
            # TELEGRAM
            # -----------------------------

            telegram_bot.bot_start()



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

                watchdog.start()

            except Exception as e:

                print(
                    "[WATCHDOG ERROR]",
                    e
                )



            # -----------------------------
            # RUN FLAG
            # -----------------------------

            self.running = True



            # -----------------------------
            # MARKET LOOP
            # -----------------------------

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


            raise e






    # =====================================
    # MARKET STREAM
    # =====================================

    def start_market_stream(self):


        def run():


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


                        self.on_candle(
                            candles
                        )


                    try:

                        watchdog.heartbeat()

                    except:

                        pass



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
    # CANDLE EVENT
    # =====================================

    def on_candle(
        self,
        candles
    ):


        if not self.running:

            return



        signal = (

            vwap_supertrend_strategy
            .analyze(
                candles
            )

        )


        if signal is None:

            return



        print(
            "[SIGNAL]",
            signal
        )



        database.save_signal(
            signal
        )



        # -----------------------------
        # EXIT
        # -----------------------------

        if signal["type"] == "EXIT":


            try:

                order_manager.close_position()

            except Exception as e:

                database.save_error(
                    str(e)
                )


            return




        # -----------------------------
        # ENTRY
        # -----------------------------

        if not risk_manager.can_trade():


            print(
                "[RISK BLOCK]"
            )


            return



        try:

            order_manager.execute(
                signal
            )


        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            database.save_error(
                str(e)
            )







    # =====================================
    # EQUITY PARSER
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
