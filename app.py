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



            if equity <= 0:

                raise Exception(
                    "INVALID EQUITY"
                )



            # -----------------------------
            # POSITION RESTORE
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
            # PRIVATE WS
            # -----------------------------

            private_ws.start()



            # -----------------------------
            # WATCHDOG
            # -----------------------------

            watchdog.start()



            # -----------------------------
            # START FLAG
            # -----------------------------

            self.running = True



            # -----------------------------
            # MARKET DATA
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


            self.stop()


            raise



    # =====================================
    # CANDLE EVENT
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



            if signal is None:

                return



            print(
                "[SIGNAL]",
                signal
            )



            # -------------------------
            # EXIT
            # -------------------------

            if signal["type"] == "EXIT":


                order_manager.close_position()


                return



            # -------------------------
            # ENTRY
            # -------------------------

            if not risk_manager.can_trade():


                print(
                    "[RISK BLOCK]"
                )


                return



            order_manager.execute(

                signal

            )



        except Exception as e:


            print(
                "[CANDLE ERROR]",
                e
            )



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



                except Exception as e:


                    print(
                        "[MARKET LOOP ERROR]",
                        e
                    )



                time.sleep(60)



            print(
                "[MARKET THREAD STOP]"
            )



        self.market_thread = threading.Thread(

            target=run,

            daemon=True

        )


        self.market_thread.start()



    # =====================================
    # EQUITY PARSER
    # =====================================

    def parse_equity(
        self,
        wallet
    ):


        try:


            # New BybitAPI format

            if "equity" in wallet:


                return float(

                    wallet["equity"]

                )



            # fallback old format

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
    # HEALTH CHECK
    # =====================================

    def health_check(self):


        try:


            if not bybit_api.ping():

                print(
                    "[HEALTH ERROR] API"
                )



        except Exception as e:


            print(
                "[HEALTH ERROR]",
                e
            )



    # =====================================
    # STOP
    # =====================================

    def stop(self):


        print(
            "[BOT STOP]"
        )


        self.running = False



        try:


            # 미체결 주문 제거

            bybit_api.cancel_all_orders()



        except Exception as e:


            print(
                "[CANCEL ERROR]",
                e
            )



        try:


            private_ws.stop()


        except Exception:


            pass



        try:


            watchdog.stop()


        except Exception:


            pass



        try:


            if self.market_thread:


                self.market_thread.join(

                    timeout=5

                )


        except Exception:


            pass



        print(
            "[BOT STOPPED]"
        )
