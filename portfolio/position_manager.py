import time


class PositionManager:


    def __init__(

        self,

        bybit_api

    ):


        self.api = bybit_api


        self.position = {

            "side": None,

            "size": 0,

            "entry_price": 0,

            "unrealized_pnl": 0,

            "updated": 0

        }



    # =====================================================
    # SYNC FROM EXCHANGE
    # =====================================================

    def sync(self):


        try:


            response = self.api.get_position()



            if not response:

                return False



            data = (

                response
                .get("result", {})
                .get("list", [])

            )


            if not data:

                self.clear()

                return True



            pos = data[0]



            size = float(

                pos.get(
                    "size",
                    0
                )

            )



            if size <= 0:


                self.clear()

                return True



            self.position = {


                "side":

                    pos.get(
                        "side"
                    ),


                "size":

                    size,


                "entry_price":

                    float(

                        pos.get(
                            "avgPrice",
                            0
                        )

                    ),


                "unrealized_pnl":

                    float(

                        pos.get(
                            "unrealisedPnl",
                            0
                        )

                    ),


                "updated":

                    time.time()

            }



            return True



        except Exception as e:


            print(

                "[POSITION SYNC ERROR]",

                e

            )


            return False



    # =====================================================
    # CURRENT POSITION
    # =====================================================

    def get_position(self):

        return self.position



    # =====================================================
    # HAS POSITION
    # =====================================================

    def has_position(self):


        return (

            self.position["size"]

            >

            0

        )



    # =====================================================
    # SIDE
    # =====================================================

    def side(self):


        return self.position["side"]



    # =====================================================
    # SIZE
    # =====================================================

    def size(self):


        return self.position["size"]



    # =====================================================
    # ENTRY PRICE
    # =====================================================

    def entry_price(self):


        return self.position["entry_price"]



    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):


        self.position = {


            "side": None,

            "size": 0,

            "entry_price": 0,

            "unrealized_pnl": 0,

            "updated": time.time()

        }



    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return self.position



position_manager = None
