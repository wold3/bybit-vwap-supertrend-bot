import time


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL,
)


from execution.order_manager import (
    order_manager
)



class ExecutionEngine:


    def __init__(self):


        self.live = LIVE_TRADING

        self.symbol = DEFAULT_SYMBOL

        self.base = BYBIT_BASE_URL


        self.last_signal_time = 0

        self.signal_cooldown = 5



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
        signal,
        qty=0.001
    ):


        print(
            "[EXECUTION SIGNAL]",
            signal
        )



        if signal not in (

            "BUY",

            "SELL"

        ):


            print(
                "[EXECUTION BLOCK] INVALID SIGNAL"
            )

            return None




        # ---------------------------------
        # SIGNAL COOLDOWN
        # ---------------------------------

        now = time.time()


        if now - self.last_signal_time < self.signal_cooldown:


            print(
                "[EXECUTION BLOCK] COOLDOWN"
            )

            return None



        self.last_signal_time = now




        # ---------------------------------
        # PAPER MODE
        # ---------------------------------

        if not self.live:


            print(
                "[PAPER MODE]",
                signal,
                qty
            )


            return {

                "retCode":0,

                "retMsg":
                "PAPER MODE"

            }




        # ---------------------------------
        # LIVE ORDER
        # ---------------------------------

        try:


            if signal == "BUY":


                result = order_manager.create_order(

                    side="Buy",

                    qty=qty

                )



            elif signal == "SELL":


                result = order_manager.create_order(

                    side="Sell",

                    qty=qty

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

            "BUY"

        )




    # =====================================================
    # TEST SELL
    # =====================================================

    def test_sell(self):


        return self.execute(

            "SELL"

        )




execution_engine = ExecutionEngine()
