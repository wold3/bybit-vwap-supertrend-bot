import time


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL,
)


from execution.order_manager import (
    order_manager,
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






    # =====================================================
    # EXECUTE SIGNAL
    # =====================================================


    def execute(
        self,
        strategy_result
    ):


        print(
            "[EXECUTION INPUT]",
            strategy_result
        )



        if strategy_result is None:


            return None





        signal = strategy_result.get(
            "signal"
        )


        qty = strategy_result.get(
            "qty",
            0
        )


        take_profit = strategy_result.get(
            "take_profit"
        )


        stop_loss = strategy_result.get(
            "stop_loss"
        )






        if signal not in (

            "BUY",

            "SELL"

        ):


            print(
                "[EXECUTION INVALID SIGNAL]"
            )


            return None






        # ---------------------------------
        # LIVE CHECK
        # ---------------------------------


        if not self.live:


            print(
                "[EXECUTION BLOCKED]"
            )


            print(
                "LIVE_TRADING=False"
            )


            return None






        side = (

            "Buy"

            if signal == "BUY"

            else

            "Sell"

        )







        try:



            result = order_manager.create_order(

                side=side,

                qty=qty,

                take_profit=take_profit,

                stop_loss=stop_loss,

            )



            print(
                "[EXECUTION RESULT]",
                result
            )



            return result





        except Exception as e:


            print(
                "[EXECUTION ERROR]",
                e
            )


            return None







    # =====================================================
    # TEST BUY
    # =====================================================


    def test_buy(self):


        return self.execute(


            {

                "signal":

                    "BUY",


                "qty":

                    0.001,


                "take_profit":

                    None,


                "stop_loss":

                    None,

            }


        )







    # =====================================================
    # TEST SELL
    # =====================================================


    def test_sell(self):


        return self.execute(


            {

                "signal":

                    "SELL",


                "qty":

                    0.001,


                "take_profit":

                    None,


                "stop_loss":

                    None,

            }


        )







execution_engine = ExecutionEngine()
