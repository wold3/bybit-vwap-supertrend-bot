import time


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    DEFAULT_QTY,
)


from execution.order_manager import (
    order_manager,
)


from position.position_manager import (
    position_manager,
)


from risk.risk_manager import (
    risk_manager,
)




class ExecutionEngine:


    def __init__(self):


        self.live = LIVE_TRADING

        self.symbol = DEFAULT_SYMBOL

        self.default_qty = DEFAULT_QTY



        print("==============================")
        print("[EXECUTION ENGINE INIT]")
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")





    # =====================================================
    # EXECUTE SIGNAL
    # =====================================================

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






        # -------------------------
        # LIVE CHECK
        # -------------------------

        if not self.live:


            print(
                "[EXECUTION BLOCKED]"
            )

            print(
                "LIVE_TRADING=False"
            )


            return {

                "retCode":0,

                "retMsg":
                "PAPER MODE"

            }







        # -------------------------
        # POSITION CHECK
        # -------------------------

        try:


            position_manager.sync()



            if position_manager.has_position():


                print(
                    "[EXECUTION BLOCK] POSITION EXISTS"
                )


                return None



        except Exception as e:


            print(
                "[POSITION CHECK ERROR]",
                e
            )







        # -------------------------
        # RISK CHECK
        # -------------------------

        qty = self.default_qty



        if not risk_manager.allow_order(
            qty
        ):


            print(
                "[EXECUTION BLOCK] RISK"
            )


            return None








        # -------------------------
        # ORDER
        # -------------------------

        side = (

            "Buy"

            if signal == "BUY"

            else "Sell"

        )





        result = order_manager.create_order(

            side=side,

            qty=qty

        )






        if result is None:


            print(
                "[EXECUTION FAILED]"
            )


            return None






        if result.get(
            "retCode"
        ) == 0:


            print(
                "[EXECUTION SUCCESS]",
                signal
            )



            risk_manager.record_order()



        else:


            print(
                "[EXECUTION ERROR]",
                result
            )





        return result






    # =====================================================
    # TEST
    # =====================================================

    def test_buy(self):


        return self.execute(
            "BUY"
        )




    def test_sell(self):


        return self.execute(
            "SELL"
        )






execution_engine = ExecutionEngine()
