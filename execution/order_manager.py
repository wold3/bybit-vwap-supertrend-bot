# execution/order_manager.py

import time
import requests


from config import (
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL,
    LIVE_TRADING,
    ORDER_RETRY
)


from portfolio.bybit_wallet import wallet



class OrderManager:


    def __init__(self):

        self.base_url = BYBIT_BASE_URL

        self.symbol = DEFAULT_SYMBOL

        self.live = LIVE_TRADING

        self.retry = ORDER_RETRY


        print("==============================")
        print("[ORDER MANAGER INIT]")
        print("BASE :", self.base_url)
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")



    # =====================================
    # EXECUTE SIGNAL
    # =====================================

    def execute(
        self,
        signal
    ):


        if not signal:

            return False



        print(
            "[ORDER SIGNAL]",
            signal
        )



        if not self.live:

            print(
                "[PAPER ORDER]",
                signal
            )

            return True



        side = signal.get(
            "side",
            ""
        )



        qty = signal.get(
            "qty",
            None
        )



        if not qty:

            print(
                "[ORDER ERROR] qty missing"
            )

            return False



        return self.place_order(
            side,
            qty
        )



    # =====================================
    # PLACE ORDER
    # =====================================

    def place_order(
        self,
        side,
        qty
    ):


        url = (
            self.base_url
            +
            "/v5/order/create"
        )



        payload = {

            "category":
                "linear",

            "symbol":
                self.symbol,

            "side":
                side,

            "orderType":
                "Market",

            "qty":
                str(qty),

        }



        for attempt in range(
            self.retry
        ):


            try:


                print(
                    "[ORDER REQUEST]",
                    payload
                )


                result = wallet.private_request(

                    method="POST",

                    endpoint="/v5/order/create",

                    body=payload

                )



                print(
                    "[ORDER RESPONSE]",
                    result
                )



                if result.get(
                    "retCode"
                ) == 0:


                    print(
                        "[ORDER SUCCESS]"
                    )

                    return True



                else:


                    print(
                        "[ORDER FAILED]",
                        result
                    )



            except Exception as e:


                print(
                    "[ORDER EXCEPTION]",
                    e
                )



            time.sleep(1)



        return False




    # =====================================
    # CANCEL ORDER
    # =====================================

    def cancel_all(
        self
    ):


        payload = {


            "category":
                "linear",


            "symbol":
                self.symbol

        }



        result = wallet.private_request(

            method="POST",

            endpoint="/v5/order/cancel-all",

            body=payload

        )


        print(
            "[CANCEL ALL]",
            result
        )


        return result




order_manager = OrderManager()
