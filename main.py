import time
import threading


from api.bybit_api import bybit_api

from execution.order_manager import order_manager

from risk.risk_manager import risk_manager

from signal.vwap_supertrend import vwap_supertrend


from config import (
    DEFAULT_SYMBOL,
    CATEGORY,
    ACCOUNT_TYPE,
)



# ==================================================
# BOT APP
# ==================================================

class TradingBot:


    def __init__(self):


        print("==============================")
        print("[APP INIT]")
        print("==============================")


        self.running = False



    # ==================================================
    # WALLET INIT
    # ==================================================

    def init_wallet(self):


        print("==============================")
        print("[WALLET INIT]")
        print(
            "ACCOUNT :",
            ACCOUNT_TYPE
        )
        print("==============================")


        wallet = bybit_api.get_wallet_balance()



        if wallet is None:

            print(
                "[WALLET INIT FAILED]"
            )

            return False



        try:


            equity = float(

                wallet
                ["result"]
                ["list"]
                [0]
                ["totalEquity"]

            )



            print(
                "[START EQUITY]",
                equity
            )



            risk_manager.initialize(

                equity

            )



            return True



        except Exception as e:


            print(
                "[WALLET PARSE ERROR]",
                e
            )


            return False




    # ==================================================
    # MARKET LOOP
    # ==================================================

    def market_loop(self):


        print(
            "[APP LOOP START]"
        )


        while self.running:


            try:



                # --------------------------
                # KLINE
                # --------------------------

                data = bybit_api.get_kline(

                    interval="1"

                )



                if data is None:


                    time.sleep(5)

                    continue




                candles = (

                    data
                    ["result"]
                    ["list"]

                )




                # --------------------------
                # SIGNAL
                # --------------------------

                signal = (

                    vwap_supertrend
                    .get_signal(
                        candles
                    )

                )



                print(

                    "[SIGNAL]",

                    signal

                )





                # --------------------------
                # EXECUTION
                # --------------------------


                if signal == "BUY":


                    order_manager.buy()



                elif signal == "SELL":


                    order_manager.sell()





                # --------------------------
                # EQUITY UPDATE
                # --------------------------


                wallet = (

                    bybit_api
                    .get_wallet_balance()

                )



                if wallet:


                    equity = float(

                        wallet
                        ["result"]
                        ["list"]
                        [0]
                        ["totalEquity"]

                    )


                    risk_manager.update_equity(

                        equity

                    )



                time.sleep(5)



            except Exception as e:


                print(

                    "[LOOP ERROR]",

                    e

                )


                time.sleep(5)




    # ==================================================
    # START
    # ==================================================

    def start(self):


        print("====================================")
        print("VWAP SUPERTREND BOT START")
        print("====================================")



        if not self.init_wallet():


            print(
                "[BOT START FAILED]"
            )

            return




        self.running = True



        print(
            "[BOT RUNNING]"
        )



        self.market_loop()





    # ==================================================
    # STOP
    # ==================================================

    def stop(self):


        self.running = False


        print(
            "[BOT STOPPED]"
        )





# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":



    bot = TradingBot()



    try:


        bot.start()



    except KeyboardInterrupt:


        print(
            "\n[MAIN SHUTDOWN]"
        )


        bot.stop()
