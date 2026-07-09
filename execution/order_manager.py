import time
import uuid


from config import (
    DEFAULT_SYMBOL,
    LIVE_TRADING,
)


from api.bybit_client import (
    bybit_client
)



class OrderManager:


    def __init__(self):


        self.symbol = DEFAULT_SYMBOL

        self.live = LIVE_TRADING


        self.last_order_time = 0

        self.cooldown = 3



        print("==============================")
        print("[ORDER MANAGER INIT]")
        print("SYMBOL :", self.symbol)
        print("LIVE :", self.live)
        print("==============================")



    # =====================================================
    # PLACE ORDER
    # =====================================================

    def place_order(
        self,
        side,
        qty,
        take_profit=None,
        stop_loss=None,
    ):


        return self.create_order(

            side,

            qty,

            take_profit,

            stop_loss

        )



    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create_order(
        self,
        side,
        qty,
        take_profit=None,
        stop_loss=None,
    ):


        now = time.time()


        if (

            now - self.last_order_time

            <

            self.cooldown

        ):


            print(
                "[ORDER BLOCK] COOLDOWN"
            )

            return None



        if not self.live:


            print(
                "[ORDER BLOCK] LIVE_TRADING=False"
            )

            return None



        order_id = (

            "VWAP_"

            +

            uuid.uuid4().hex[:8]

        )



        params = {


            "category":

                "linear",


            "symbol":

                self.symbol,


            "side":

                side,


            "positionIdx":

                0,


            "orderType":

                "Market",


            "qty":

                str(qty),


            "orderLinkId":

                order_id

        }



        if take_profit is not None:

            params["takeProfit"] = str(
                take_profit
            )



        if stop_loss is not None:

            params["stopLoss"] = str(
                stop_loss
            )



        print("==============================")
        print("[ORDER REQUEST]")
        print(params)
        print("==============================")



        result = bybit_client.post(

            "/v5/order/create",

            params

        )



        print(
            "[ORDER RESULT]",
            result
        )



        if result is None:

            return None



        if result.get(
            "retCode"
        ) != 0:


            print(
                "[ORDER FAILED]",
                result.get(
                    "retMsg"
                )
            )


            return result



        self.last_order_time = time.time()



        print(
            "[ORDER SUCCESS]",
            order_id
        )


        return result



    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(
        self,
        side,
        qty
    ):


        close_side = (

            "Sell"

            if side == "Buy"

            else

            "Buy"

        )



        params = {


            "category":

                "linear",


            "symbol":

                self.symbol,


            "side":

                close_side,


            "positionIdx":

                0,


            "orderType":

                "Market",


            "qty":

                str(qty),


            "reduceOnly":

                True

        }



        return bybit_client.post(

            "/v5/order/create",

            params

        )



    # =====================================================
    # CANCEL ALL
    # =====================================================

    def cancel_all(self):


        params = {


            "category":

                "linear",


            "symbol":

                self.symbol

        }


        return bybit_client.post(

            "/v5/order/cancel-all",

            params

        )




order_manager = OrderManager()
