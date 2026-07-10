import time


from config import (
    DEFAULT_SYMBOL,
)


from api.bybit_client import (
    bybit_client,
)





class PositionManager:



    def __init__(self):


        self.symbol = DEFAULT_SYMBOL



        self.current = {


            "side": None,


            "size": 0,


            "avg_price": 0,


            "unrealised_pnl": 0,


            "position_idx": 0,

        }



        print("==============================")
        print("[POSITION MANAGER READY]")
        print("SYMBOL :", self.symbol)
        print("==============================")









    # =====================================================
    # SYNC
    # =====================================================

    def sync(self):


        try:



            params = {


                "category":

                    "linear",


                "symbol":

                    self.symbol,

            }






            response = bybit_client.get(

                "/v5/position/list",

                params

            )






            if not response:


                return self.current






            if response.get(
                "retCode"
            ) != 0:


                print(

                    "[POSITION API ERROR]",

                    response

                )


                return self.current







            positions = (

                response

                .get("result", {})

                .get("list", [])

            )







            if not positions:


                self.clear()


                return self.current







            # One-way mode 기준

            pos = positions[0]








            size = float(

                pos.get(

                    "size",

                    0

                )

            )







            if size <= 0:


                self.clear()


                return self.current







            self.current = {


                "side":

                    pos.get(
                        "side"
                    ),



                "size":

                    size,



                "avg_price":

                    float(

                        pos.get(

                            "avgPrice",

                            0

                        )

                    ),



                "unrealised_pnl":

                    float(

                        pos.get(

                            "unrealisedPnl",

                            0

                        )

                    ),



                "position_idx":

                    int(

                        pos.get(

                            "positionIdx",

                            0

                        )

                    ),


            }







            print(

                "[POSITION UPDATE]",

                self.current

            )



            return self.current








        except Exception as e:


            print(

                "[POSITION SYNC ERROR]",

                e

            )


            return self.current











    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):


        self.current = {


            "side": None,


            "size": 0,


            "avg_price": 0,


            "unrealised_pnl": 0,


            "position_idx": 0,


        }











    # =====================================================
    # CHECK
    # =====================================================

    def has_position(self):


        return (

            self.current["size"]

            >

            0

        )









    def get_side(self):


        return self.current["side"]







    def get_size(self):


        return self.current["size"]







    def get_avg_price(self):


        return self.current["avg_price"]







    def get_pnl(self):


        return self.current["unrealised_pnl"]










    # =====================================================
    # MONITOR
    # =====================================================

    def monitor(self):


        print(
            "[POSITION MONITOR START]"
        )



        while True:


            try:


                self.sync()



            except Exception as e:


                print(
                    "[POSITION MONITOR ERROR]",
                    e
                )



            time.sleep(5)











position_manager = PositionManager()
