import time
import traceback


from api.bybit_api import bybit_api

from execution.order_manager import order_manager

from execution.position_manager import position_manager

from risk.risk_manager import risk_manager

from signal.vwap_supertrend import vwap_supertrend


from config import (
    ACCOUNT_TYPE,
    LEVERAGE,
)



# ==================================================
# TRADING BOT
# ==================================================

class TradingBot:


    def __init__(self):


        self.running = False


        print("==============================")
        print("[APP INIT]")
        print("==============================")




    # ==================================================
    # INIT
    # ==================================================

    def initialize(self):


        try:


            print("==============================")
            print("[SYSTEM INITIALIZE]")
            print("==============================")



            # leverage

            bybit_api.set_leverage(

                LEVERAGE

            )



            # wallet

            wallet = (

                bybit_api
                .get_wallet_balance()

            )



            if wallet is None:


                print(
                    "[WALLET INIT FAILED]"
                )

                return False




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



            # risk init

            risk_manager.initialize(

                equity

            )



            print(

                "[RISK INIT OK]"

            )



            print("==============================")
            print("[INIT COMPLETE]")
            print("==============================")


            return True




        except Exception as e:


            print(
                "[INIT ERROR]",
                e
            )


            traceback.print_exc()


            return False




    # ==================================================
    # PRICE DATA
    # ==================================================

    def get_prices(self):


        try:


            result = bybit_api.get_kline(

                interval="1",

                limit=200

            )



            if result is None:

                return None



            candles = (

                result
                ["result"]
                ["list"]

            )



            prices = []



            for candle in candles:


                prices.append(

                    float(
                        candle[4]
                    )

                )



            return candles, prices



        except Exception as e:


            print(
                "[PRICE ERROR]",
                e
            )


            return None




    # ==================================================
    # LOOP
    # ==================================================

    def run(self):


        if not self.initialize():

            return



        self.running = True



        print("====================================")
        print("VWAP SUPERTREND BOT START")
        print("====================================")

        print(
            "[BOT RUNNING]"
        )



        while self.running:



            try:


                data = self.get_prices()



                if data is None:


                    time.sleep(5)

                    continue




                candles, prices = data




                # ----------------------------------
                # EXIT CHECK
                # ----------------------------------

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




                # ----------------------------------
                # SIGNAL
                # ----------------------------------

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





                # ----------------------------------
                # ORDER
                # ----------------------------------

                if signal == "BUY":


                    order_manager.buy()



                elif signal == "SELL":


                    order_manager.sell()




                # ----------------------------------
                # RISK UPDATE
                # ----------------------------------

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

                    "[LOOP ERROR]",

                    e

                )


                traceback.print_exc()



                time.sleep(5)





    # ==================================================
    # STOP
    # ==================================================

    def stop(self):


        print(
            "[BOT STOPPING]"
        )


        self.running = False


        print(
            "[BOT STOPPED]"
        )





# ==================================================
# START
# ==================================================

if __name__ == "__main__":


    bot = TradingBot()


    bot.run()
