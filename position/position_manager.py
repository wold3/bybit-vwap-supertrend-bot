import time


from config import (
    DEFAULT_SYMBOL
)


from api.bybit_client import bybit_client





class PositionManager:



    def __init__(self):


        self.symbol = DEFAULT_SYMBOL


        self.current = {


            "side": None,

            "size": 0,

            "avg_price": 0


        }



        print(
            "[POSITION MANAGER READY]"
        )







    # =================================
    # SYNC POSITION
    # =================================


    def sync(self):


        try:


            params = {


                "category":

                "linear",



                "symbol":

                self.symbol


            }





            result = bybit_client.get(

                "/v5/position/list",

                params

            )





            print(
                "[POSITION RESPONSE]",
                result
            )





            if not result:


                return self.current





            if result.get(
                "retCode"
            ) != 0:


                return self.current






            data = result["result"]["list"]






            if len(data) == 0:


                self.clear()


                return self.current






            pos = data[0]





            size = float(

                pos.get(

                    "size",

                    0

                )

            )





            side = pos.get(
                "side"
            )



            avg = float(

                pos.get(

                    "avgPrice",

                    0

                )

            )







            if size == 0:



                self.clear()



            else:



                self.current = {


                    "side":

                    side,



                    "size":

                    size,



                    "avg_price":

                    avg


                }





            print(

                "[CURRENT POSITION]",

                self.current

            )



            return self.current





        except Exception as e:



            print(

                "[POSITION ERROR]",

                e

            )



            return self.current







    # =================================
    # CLEAR
    # =================================


    def clear(self):


        self.current = {


            "side": None,


            "size": 0,


            "avg_price": 0


        }







    # =================================
    # CHECK
    # =================================


    def has_position(self):


        return (

            self.current["size"]

            >

            0

        )






    def side(self):


        return self.current["side"]







    def size(self):


        return self.current["size"]







    def price(self):


        return self.current["avg_price"]







    # =================================
    # REFRESH LOOP
    # =================================


    def monitor(self):


        while True:


            self.sync()


            time.sleep(5)








position_manager = PositionManager()
