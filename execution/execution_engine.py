# execution/execution_engine.py

import time


from config import (
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL,
    LIVE_TRADING
)


from portfolio.bybit_wallet import wallet



class ExecutionEngine:


    def __init__(self):


        self.base_url = BYBIT_BASE_URL


        self.symbol = DEFAULT_SYMBOL


        self.live = LIVE_TRADING



        print("==============================")
        print("[EXECUTION ENGINE INIT]")
        print("BASE :", self.base_url)
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")



    # =====================================
    # EXECUTE
    # =====================================

    def execute(
        self,
        signal
    ):


        if not signal:


            return False



        print(
            "[EXECUTION SIGNAL]",
            signal
        )



        if not self.live:


            print(
                "[SIMULATION MODE]",
                signal
            )


            return True



        side = signal.get(
            "side"
        )


        qty = signal.get(
            "qty"
        )



        if not side or not qty:


            print(
                "[EXECUTION ERROR] Invalid signal"
            )


            return False



        return self.market_order(

            side,

            qty

        )



    # =====================================
    # MARKET ORDER
    # =====================================

    def market_order(
        self,
        side,
        qty
    ):



        endpoint = (
            "/v5/order/create"
        )



        body = {


            "category":
                "linear",


            "symbol":
                self.symbol,


            "side":
                side,


            "orderType":
                "Market",


            "qty":
                str(qty)


        }



        print(
            "[MARKET ORDER]",
            body
        )



        try:


            response = wallet.private_request(

                method="POST",

                endpoint=endpoint,

                body=body

            )



            print(
                "[BYBIT ORDER RESPONSE]",
                response
            )



            if response.get(
                "retCode"
            ) == 0:


                print(
                    "[ORDER SUCCESS]"
                )


                return True



            else:


                print(
                    "[ORDER FAILED]",
                    response
                )


                return False



        except Exception as e:


            print(
                "[EXECUTION ERROR]",
                e
            )


            return False




    # =====================================
    # CANCEL ALL
    # =====================================

    def cancel_all_orders(
        self
    ):


        body = {


            "category":
                "linear",


            "symbol":
                self.symbol


        }



        try:


            result = wallet.private_request(

                method="POST",

                endpoint="/v5/order/cancel-all",

                body=body

            )



            print(
                "[CANCEL RESULT]",
                result
            )


            return result



        except Exception as e:


            print(
                "[CANCEL ERROR]",
                e
            )


            return None




    # =====================================
    # POSITION CLOSE
    # =====================================

    def close_position(
        self
    ):


        print(
            "[CLOSE POSITION REQUEST]"
        )


        return self.cancel_all_orders()




execution_engine = ExecutionEngine()
