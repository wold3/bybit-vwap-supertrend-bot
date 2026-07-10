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


        print("==============================")
        print("[EXECUTION ORDER MANAGER INIT]")
        print("CATEGORY :", self.category)
        print("SYMBOL :", self.symbol)
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







            if not risk_manager.allow_order(qty):


                print(
                    "[ORDER BLOCKED]"
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

                "[ORDER REQUEST]",

                params

            )








            result = bybit_client.post(

                "/v5/order/create",

                params

            )






            if not result:


                return None







            if result.get(

                "retCode"

            ) != 0:



                print(

                    "[ORDER FAILED]",

                    result

                )


                return None







            risk_manager.record_order()



            print(

                "[ORDER SUCCESS]",

                result

            )



            return result







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
    # CLOSE
    # =====================================================

    def close(
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

            "[CLOSE REQUEST]",

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
