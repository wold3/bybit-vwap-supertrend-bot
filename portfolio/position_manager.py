from api.bybit_api import bybit_api

from config import DEFAULT_SYMBOL



class PositionManager:


    def __init__(self):


        self.position = {

            "side": None,

            "size": 0,

            "entry_price": 0,

            "unrealized_pnl": 0

        }



    # =====================================
    # SYNC FROM EXCHANGE
    # =====================================

    def sync(self):


        try:


            response = (

                bybit_api
                .get_position()

            )


            if not response:

                return False



            positions = (

                response
                ["result"]
                ["list"]

            )



            for pos in positions:



                size = float(

                    pos["size"]

                )



                if size > 0:



                    self.position = {


                        "side":
                            pos["side"],


                        "size":
                            size,


                        "entry_price":
                            float(
                                pos["avgPrice"]
                            ),


                        "unrealized_pnl":
                            float(
                                pos["unrealisedPnl"]
                            )


                    }


                    return True




            # NO POSITION


            self.clear()


            return True



        except Exception as e:


            print(

                "[POSITION SYNC ERROR]",

                e

            )


            return False



    # =====================================
    # GET
    # =====================================

    def get(self):

        return self.position



    # =====================================
    # CHECK
    # =====================================

    def has_position(self):


        return (

            self.position["size"] > 0

        )



    def side(self):


        return self.position["side"]



    # =====================================
    # CLEAR
    # =====================================

    def clear(self):


        self.position = {


            "side": None,

            "size": 0,

            "entry_price": 0,

            "unrealized_pnl": 0


        }



    # =====================================
    # UPDATE
    # =====================================

    def update_fill(

        self,

        side,

        qty,

        price

    ):


        self.position = {


            "side": side,

            "size": qty,

            "entry_price": price,

            "unrealized_pnl":0


        }



# Singleton

position_manager = PositionManager()
