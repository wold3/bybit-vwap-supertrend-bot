import time
import uuid


from config import (
    DEFAULT_SYMBOL,
    LIVE_TRADING,
)


from api.bybit_client import bybit_client



class OrderManager:


    def __init__(self):


        self.symbol = DEFAULT_SYMBOL

        self.live = LIVE_TRADING


        self.last_order_time = 0

        self.order_cooldown = 3


        self.active_orders = {}



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
        stop_loss=None
    ):



        print(
            "[CREATE ORDER]",
            side,
            qty
        )



        # ---------------------------------
        # PAPER MODE
        # ---------------------------------

        if not self.live:


            print(
                "[ORDER BLOCK]",
                "LIVE_TRADING=False"
            )


            return {


                "retCode":0,


                "retMsg":

                "PAPER MODE"



            }




        # ---------------------------------
        # VALIDATE
        # ---------------------------------

        if side not in (

            "Buy",

            "Sell"

        ):


            print(
                "[ORDER ERROR] INVALID SIDE"
            )


            return None




        try:

            qty = float(qty)


        except:


            print(
                "[ORDER ERROR] INVALID QTY"
            )

            return None



        if qty <= 0:


            print(
                "[ORDER ERROR] ZERO QTY"
            )


            return None





        # ---------------------------------
        # COOLDOWN
        # ---------------------------------

        now = time.time()


        if now - self.last_order_time < self.order_cooldown:


            print(
                "[ORDER BLOCK] COOLDOWN"
            )


            return None






        # ---------------------------------
        # ORDER ID
        # ---------------------------------

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





        # ---------------------------------
        # TP SL
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
        print("[BYBIT ORDER REQUEST]")
        print(params)
        print("==============================")





        try:



            result = bybit_client.post(

                "/v5/order/create",

                params

            )





            print(
                "[BYBIT ORDER RESPONSE]",
                result
            )





            if result is None:


                print(
                    "[ORDER FAILED] NO RESPONSE"
                )


                return None






            if result.get(
                "retCode"
            ) != 0:



                print(
                    "[ORDER FAILED]",
                    result.get("retCode"),
                    result.get("retMsg")
                )


                return result





            self.last_order_time = time.time()



            self.active_orders[order_id] = {


                "side":

                side,


                "qty":

                qty,


                "time":

                time.time()



            }





            print(
                "[ORDER SUCCESS]",
                order_id
            )



            return result






        except Exception as e:



            print(
                "[ORDER EXCEPTION]",
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

            True



        }




        print(
            "[CLOSE POSITION]",
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





    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "symbol":

            self.symbol,


            "live":

            self.live,


            "active_orders":

            self.active_orders,


            "last_order":

            self.last_order_time


        }





order_manager = OrderManager()
