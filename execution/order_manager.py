import time
import uuid


from config import (
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL,
    LIVE_TRADING
)


from api.bybit_client import bybit_client





class OrderManager:



    def __init__(self):


        self.base = BYBIT_BASE_URL

        self.symbol = DEFAULT_SYMBOL


        self.live = LIVE_TRADING


        self.last_order = None


        print("==============================")
        print("[ORDER MANAGER INIT]")
        print("BASE :", self.base)
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")







    # =================================
    # CREATE ORDER
    # =================================


    def create_order(
            self,
            side,
            qty,
            take_profit=None,
            stop_loss=None
    ):


        # -----------------------------
        # duplicate protection
        # -----------------------------


        now = time.time()



        if self.last_order:


            if now - self.last_order < 3:


                print(
                    "[ORDER BLOCK] DUPLICATE"
                )


                return None




        self.last_order = now






        order_link_id = (

            "VWAP_"

            + str(uuid.uuid4())[:8]

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

            order_link_id


        }






        print("==============================")
        print("[ORDER REQUEST]")
        print(params)
        print("==============================")






        # -----------------------------
        # TP SL
        # -----------------------------


        if take_profit:


            params["takeProfit"] = str(
                take_profit
            )



        if stop_loss:


            params["stopLoss"] = str(
                stop_loss
            )







        try:



            result = bybit_client.post(

                "/v5/order/create",

                params

            )




            print(
                "[ORDER RESPONSE]",
                result
            )



            return result





        except Exception as e:



            print(
                "[ORDER ERROR]",
                e
            )


            return None







    # =================================
    # CLOSE POSITION
    # =================================


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
            "[CLOSE POSITION]",
            params
        )





        try:



            result = bybit_client.post(

                "/v5/order/create",

                params

            )



            print(

                "[CLOSE RESPONSE]",

                result

            )



            return result




        except Exception as e:



            print(
                "[CLOSE ERROR]",
                e
            )


            return None







    # =================================
    # CANCEL ALL
    # =================================


    def cancel_all(self):


        params = {


            "category":

            "linear",



            "symbol":

            self.symbol


        }





        try:


            result = bybit_client.post(

                "/v5/order/cancel-all",

                params

            )


            print(

                "[CANCEL ALL]",

                result

            )



            return result




        except Exception as e:



            print(
                "[CANCEL ERROR]",
                e
            )


            return None











order_manager = OrderManager()
