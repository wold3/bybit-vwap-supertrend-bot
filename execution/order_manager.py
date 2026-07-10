import time
import uuid


from config import (
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL,
    LIVE_TRADING,
)


from api.bybit_client import bybit_client






class OrderManager:



    def __init__(self):


        self.base = BYBIT_BASE_URL

        self.symbol = DEFAULT_SYMBOL

        self.live = LIVE_TRADING



        self.last_order_time = 0

        self.duplicate_seconds = 3



        print("==============================")
        print("[ORDER MANAGER INIT]")
        print("BASE :", self.base)
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")







    # =====================================================
    # PLACE ORDER (MAIN)
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



        # -------------------------
        # Duplicate Protection
        # -------------------------

        if (

            now - self.last_order_time

            <

            self.duplicate_seconds

        ):


            print(
                "[ORDER BLOCK] DUPLICATE"
            )


            return None








        # -------------------------
        # LIVE CHECK
        # -------------------------

        if not self.live:


            print(
                "[ORDER BLOCKED] LIVE_TRADING=False"
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






        # -------------------------
        # TP SL
        # -------------------------

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



            result = bybit_client.post(

                "/v5/order/create",

                params

            )





            print(

                "[ORDER RESPONSE]",

                result

            )






            if not result:


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

                True,


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

                self.symbol,


        }



        return bybit_client.post(

            "/v5/order/cancel-all",

            params

        )









order_manager = OrderManager()
