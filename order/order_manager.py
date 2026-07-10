from config import (
    DEFAULT_SYMBOL,
    CATEGORY,
    DEFAULT_QTY,
)


from api.bybit_client import (
    bybit_client,
)


from risk.risk_manager import (
    risk_manager,
)





class OrderManager:



    def __init__(self):


        self.symbol = DEFAULT_SYMBOL

        self.category = CATEGORY


        self.live = True


        print("==============================")
        print("[ORDER MANAGER INIT]")
        print("SYMBOL :", self.symbol)
        print("CATEGORY :", self.category)
        print("==============================")









    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create_order(
        self,
        side,
        qty=None
    ):


        try:



            if qty is None:

                qty = DEFAULT_QTY






            qty = float(qty)







            # Risk Check

            if not risk_manager.allow_order(qty):


                print(
                    "[ORDER BLOCKED BY RISK]"
                )


                return None







            params = {



                "category":

                    self.category,



                "symbol":

                    self.symbol,



                "side":

                    side,



                "orderType":

                    "Market",



                "qty":

                    str(qty),



                "timeInForce":

                    "IOC",



            }








            print(
                "[ORDER SEND]",
                params
            )







            response = bybit_client.post(

                "/v5/order/create",

                params

            )






            if not response:


                return None








            if response.get(
                "retCode"
            ) != 0:


                print(

                    "[ORDER ERROR]",

                    response

                )


                return None







            risk_manager.record_order()





            print(

                "[ORDER SUCCESS]",

                response

            )



            return response







        except Exception as e:


            print(

                "[ORDER EXCEPTION]",

                e

            )


            return None










    # =====================================================
    # BUY
    # =====================================================

    def buy(
        self,
        qty=None
    ):


        return self.create_order(

            "Buy",

            qty

        )









    # =====================================================
    # SELL
    # =====================================================

    def sell(
        self,
        qty=None
    ):


        return self.create_order(

            "Sell",

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

            else

            "Buy"

        )




        params = {


            "category":

                self.category,


            "symbol":

                self.symbol,


            "side":

                close_side,


            "orderType":

                "Market",


            "qty":

                str(qty),


            "reduceOnly":

                True,


        }




        print(

            "[CLOSE ORDER]",

            params

        )





        return bybit_client.post(

            "/v5/order/create",

            params

        )












    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "symbol":

                self.symbol,


            "category":

                self.category,


        }











order_manager = OrderManager()
