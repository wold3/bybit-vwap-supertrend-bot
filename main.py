import time


from api.bybit_api import bybit_api

from execution.order_manager import order_manager

from execution.position_manager import position_manager

from risk.risk_manager import risk_manager

from signal.vwap_supertrend import vwap_supertrend


from config import (
    ACCOUNT_TYPE,
    DEFAULT_SYMBOL,
)



class TradingBot:


    def __init__(self):


        print("==============================")
        print("[APP INIT]")
        print("==============================")


        self.running = False




    # ==========================================
    # WALLET INIT
    # ==========================================

    def initialize_wallet(self):


        print("==============================")
        print("[WALLET INIT]")
        print(
            "ACCOUNT :",
            ACCOUNT_TYPE
        )
        print("==============================")



        wallet = bybit_api.get_wallet_balance()



        if wallet is None:

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

                "[WALLET ERROR]",

                e

            )


            return False




    # ==========================================
    # MAIN LOOP
    # ==========================================

    def run(self):


        print("====================================")
        print("VWAP SUPERTREND BOT START")
        print("====================================")



        if not self.initialize_wallet():


            print(
                "[INIT FAILED]"
            )

            return




        self.running = True



        print(
            "[BOT RUNNING]"
        )



        while self.running:



            try:



                # ==================================
                # GET KLINE
                # ==================================

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




                prices = []



                for c in candles:


                    prices.append(

                        float(c[4])

                    )





                # ==================================
                # POSITION EXIT CHECK
                # ==================================

                exit_signal = (

                    position_manager
                    .evaluate_exit(

                        prices

                    )

                )



                if exit_signal:



                    print(

                        "[EXIT SIGNAL]",

                        exit_signal

                    )



                    position_manager.close_position()



                    time.sleep(5)

                    continue





                # ==================================
                # SIGNAL CHECK
                # ==================================

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





                # ==================================
                # ORDER EXECUTION
                # ==================================

                if signal == "BUY":



                    order_manager.buy()




                elif signal == "SELL":



                    order_manager.sell()





                # ==================================
                # UPDATE RISK
                # ==================================

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



            except KeyboardInterrupt:



                self.stop()



            except Exception as e:



                print(

                    "[MAIN LOOP ERROR]",

                    e

                )



                time.sleep(5)






    # ==========================================
    # STOP
    # ==========================================

    def stop(self):


        print(
            "[BOT STOPPING]"
        )


        self.running = False



        print(
            "[BOT STOPPED]"
        )






# ==========================================
# START
# ==========================================

if __name__ == "__main__":


    bot = TradingBot()


    bot.run()
