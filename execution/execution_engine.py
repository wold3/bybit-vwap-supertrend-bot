import time


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL,
    DEFAULT_QTY,
)


from execution.order_manager import (
    order_manager
)



class ExecutionEngine:


    def __init__(self):

        self.live = LIVE_TRADING

        self.symbol = DEFAULT_SYMBOL

        self.base = BYBIT_BASE_URL


        print("==============================")
        print("[EXECUTION ENGINE INIT]")
        print("BASE :", self.base)
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")



    # =================================
    # SIGNAL EXECUTION
    # =================================

    def execute(
        self,
        signal
    ):


        print(
            "[EXECUTION SIGNAL]",
            signal
        )



        if signal not in (
            "BUY",
            "SELL"
        ):

            return None



        # -----------------------------
        # LIVE CHECK
        # -----------------------------

        if not self.live:


            print(
                "[EXECUTION BLOCKED]"
            )


            print(
                "LIVE_TRADING=False"
            )


            return None




        qty = DEFAULT_QTY



        # -----------------------------
        # BUY
        # -----------------------------

        if signal == "BUY":


            result = order_manager.create_order(

                side="Buy",

                qty=qty

            )


            return result




        # -----------------------------
        # SELL
        # -----------------------------

        if signal == "SELL":


            result = order_manager.create_order(

                side="Sell",

                qty=qty

            )


            return result




        return None





    # =================================
    # TEST
    # =================================

    def test_buy(self):


        print(
            "[TEST BUY]"
        )


        return self.execute(
            "BUY"
        )




    def test_sell(self):


        print(
            "[TEST SELL]"
        )


        return self.execute(
            "SELL"
        )





execution_engine = ExecutionEngine()
