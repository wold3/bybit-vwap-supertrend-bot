import time


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL
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



        if signal == "BUY":

            return order_manager.create_order(

                "Buy",

                0.001

            )



        if signal == "SELL":

            return order_manager.create_order(

                "Sell",

                0.001

            )



    # =================================
    # TEST ORDER
    # =================================

    def test_buy(self):

        return self.execute(
            "BUY"
        )


    def test_sell(self):

        return self.execute(
            "SELL"
        )



execution_engine = ExecutionEngine()
