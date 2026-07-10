# app.py


import time
import threading



from api.bybit_api import (
    bybit_api
)


from risk.risk_manager import (
    risk_manager
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


from services.telegram_bot import (
    telegram_bot
)





class TradingApp:



    def __init__(self):


        self.running = False


        self.market_thread = None



    # ==================================================
    # START
    # ==================================================

    def start(self):


        print("==============================")
        print("[TRADING APP START]")
        print("==============================")



        try:



            # ------------------------------------------
            # 1. API CHECK
            # ------------------------------------------

            if not bybit_api.ping():


                raise Exception(

                    "BYBIT CONNECTION FAILED"

                )



            print(
                "[API OK]"
            )



            # ------------------------------------------
            # 2. WALLET
            # ------------------------------------------

            wallet = (

                bybit_api
                .get_wallet_balance()

            )



            if wallet is None:


                raise Exception(

                    "WALLET LOAD FAILED"

                )



            equity = (

                self.parse_equity(

                    wallet

                )

            )



            if equity <= 0:


                raise Exception(

                    "INVALID EQUITY"

                )



            print(

                "[EQUITY]",

                equity

            )



            # ------------------------------------------
            # 3. POSITION RESTORE
            # ------------------------------------------

            position_manager.sync()



            print(

                "[POSITION]",

                position_manager.status()

            )



            # ------------------------------------------
            # 4. RISK INIT
            # ------------------------------------------

            risk_manager.initialize(

                equity

            )



            # ------------------------------------------
            # 5. LEVERAGE
            # ------------------------------------------

            bybit_api.set_leverage()



            # ------------------------------------------
            # 6. PRIVATE WS
            # ------------------------------------------

            private_ws.start()



            # ------------------------------------------
            # 7. WATCHDOG
            # ------------------------------------------

            watchdog.start()



            # ------------------------------------------
            # 8. TELEGRAM
            # ------------------------------------------

            telegram_bot.start()



            # ------------------------------------------
            # 9. START
            # ------------------------------------------

            self.running = True



            self.start_market_stream()



            print("==============================")
            print("[BOT READY]")
            print("==============================")



        except Exception as e:


            print(

                "[START ERROR]",

                e

            )


            self.stop()


            raise




    # ==================================================
    # MARKET LOOP
    # ==================================================

    def start_market_stream(self):


        def loop():


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

                        "[MARKET ERROR]",

                        e

                    )



                time.sleep(60)



            print(

                "[MARKET THREAD END]"

            )




        self.market_thread = threading.Thread(

            target=loop,

            daemon=True

        )



        self.market_thread.start()





    # ==================================================
    # CANDLE EVENT
    # ==================================================

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



            # ----------------------------------
            # EXIT
            # ----------------------------------

            if signal["type"] == "EXIT":



                order_manager.close_position()



                return




            # ----------------------------------
            # ENTRY
            # ----------------------------------


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

                "[CANDLE PROCESS ERROR]",

                e

            )




    # ==================================================
    # EQUITY PARSER
    # ==================================================

    def parse_equity(
        self,
        wallet
    ):


        try:



            # New format


            if "equity" in wallet:



                return float(

                    wallet["equity"]

                )




            # Bybit V5 format



            return float(

                wallet

                ["result"]

                ["list"][0]

                ["totalEquity"]

            )



        except Exception as e:



            print(

                "[EQUITY ERROR]",

                e

            )


            return 0




    # ==================================================
    # STOP
    # ==================================================

    def stop(self):


        print(

            "[APP STOP]"

        )



        self.running = False



        try:


            bybit_api.cancel_all_orders()



        except Exception:


            pass




        try:


            private_ws.stop()



        except Exception:


            pass




        try:


            watchdog.stop()



        except Exception:


            pass




        try:


            telegram_bot.stop()



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

            "[APP STOPPED]"

        )
