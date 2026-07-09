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


        self.duplicate_seconds = 3



        print("==============================")
        print("[ORDER MANAGER INIT]")
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")




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

            self.duplicate_seconds

        ):


            print(
                "[ORDER BLOCK] DUPLICATE"
            )


            return None





        order_id = (
            "VWAP_"
            +
            uuid.uuid4().hex[:10]
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


            params[
                "takeProfit"
            ] = str(
                take_profit
            )



        if stop_loss is not None:


            params[
                "stopLoss"
            ] = str(
                stop_loss
            )





        print("==============================")
        print("[ORDER REQUEST]")
        print(params)
        print("==============================")





        try:


            if not self.live:


                print(
                    "[PAPER MODE] ORDER BLOCKED"
                )


                return {

                    "retCode":0,

                    "retMsg":
                    "PAPER MODE",

                    "result":
                    {}

                }







            result = bybit_client.post(

                "/v5/order/create",

                params

            )





            print(
                "[ORDER RESPONSE]",
                result
            )





            if result is None:


                return None





            if result.get(
                "retCode"
            ) != 0:


                print(
                    "[ORDER FAILED]",
                    result
                )


                return result






            self.last_order_time = time.time()





            print(
                "[ORDER SUCCESS]",
                order_id
            )



            return result






        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return None







    # =====================================================
    # COMPATIBILITY
    # =====================================================

    def place_order(
        self,
        side,
        qty
    ):


        return self.create_order(

            side,

            qty

        )








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

            else "Buy"

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





        print(
            "[CLOSE REQUEST]",
            params
        )




        try:


            return bybit_client.post(

                "/v5/order/create",

                params

            )



        except Exception as e:


            print(
                "[CLOSE ERROR]",
                e
            )


            return None






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




        try:


            return bybit_client.post(

                "/v5/order/cancel-all",

                params

            )



        except Exception as e:


            print(
                "[CANCEL ERROR]",
                e
            )


            return None






order_manager = OrderManager()
