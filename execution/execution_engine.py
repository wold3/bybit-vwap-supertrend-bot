import time


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
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


        print("==============================")
        print("[EXECUTION ENGINE READY]")
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")



    # =====================================================
    # EXECUTE SIGNAL
    # =====================================================

    def execute(
        self,
        signal,
        qty=0.001,
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



        # ---------------------------------
        # LIVE CHECK
        # ---------------------------------

        if not self.live:


            print(
                "[EXECUTION BLOCK] LIVE=False"
            )

            return None



        # ---------------------------------
        # POSITION CHECK
        # ---------------------------------

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



        # ---------------------------------
        # RISK CHECK
        # ---------------------------------

        if not risk_manager.allow_order(qty):


            print(
                "[EXECUTION BLOCK] RISK"
            )


            return None



        side = (

            "Buy"

            if signal == "BUY"

            else

            "Sell"

        )



        # ---------------------------------
        # ORDER
        # ---------------------------------

        result = order_manager.create_order(

            side=side,

            qty=qty

        )



        if result and result.get(
            "retCode"
        ) == 0:


            print(
                "[EXECUTION SUCCESS]",
                signal
            )


            risk_manager.record_order()



        else:


            print(
                "[EXECUTION FAILED]",
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
