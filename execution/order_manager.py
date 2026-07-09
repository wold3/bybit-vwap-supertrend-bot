import time
import uuid


from config import (
    DEFAULT_SYMBOL,
)


from api.bybit_client import (
    bybit_client,
)





class OrderManager:


    def __init__(self):


        self.symbol = DEFAULT_SYMBOL


        self.last_order_time = 0


        self.order_cooldown = 3



        print("==============================")
        print("[ORDER MANAGER INIT]")
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



        # ---------------------------------
        # DUPLICATE PROTECTION
        # ---------------------------------


        if (

            now - self.last_order_time

            <

            self.order_cooldown

        ):


            print(
                "[ORDER BLOCK] COOLDOWN"
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

                order_id,

        }





        # ---------------------------------
        # TP / SL
        # ---------------------------------


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







        try:



            response = bybit_client.post(

                "/v5/order/create",

                params

            )




            print(
                "[ORDER RESPONSE]",
                response
            )





            if response is None:


                return None





            if response.get(
                "retCode"
            ) != 0:



                print(

                    "[ORDER FAILED]",

                    response.get(
                        "retCode"
                    ),

                    response.get(
                        "retMsg"
                    )

                )


                return response






            self.last_order_time = time.time()



            print(
                "[ORDER SUCCESS]",
                order_id
            )



            return response





        except Exception as e:


            print(
                "[ORDER ERROR]",
                e
            )


            return None









    # =====================================================
    # CLOSE POSITION
    # =====================================================


    def close_position(
        self,
        side,
        qty,
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

                True,

        }





        print(
            "[CLOSE REQUEST]",
            params
        )






        try:



            response = bybit_client.post(

                "/v5/order/create",

                params

            )



            print(
                "[CLOSE RESPONSE]",
                response
            )



            return response





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

                self.symbol,

        }





        try:


            response = bybit_client.post(

                "/v5/order/cancel-all",

                params

            )



            print(
                "[CANCEL ALL]",
                response
            )


            return response





        except Exception as e:


            print(
                "[CANCEL ERROR]",
                e
            )


            return None









order_manager = OrderManager()
