import time

from config import DEFAULT_SYMBOL

from api.bybit_client import bybit_client



class PositionManager:


    def __init__(self):

        self.symbol = DEFAULT_SYMBOL


        self.current = {

            "side": None,

            "size": 0,

            "avg_price": 0,

            "unrealised_pnl": 0

        }


        print("==============================")
        print("[POSITION MANAGER READY]")
        print("SYMBOL :", self.symbol)
        print("==============================")



    # =====================================
    # SYNC POSITION
    # =====================================

    def sync(self):

        try:


            params = {

                "category":
                    "linear",

                "symbol":
                    self.symbol

            }



            response = bybit_client.get(

                "/v5/position/list",

                params

            )



            if not response:

                return self.current



            if response.get("retCode") != 0:

                print(
                    "[POSITION API ERROR]",
                    response
                )

                return self.current



            positions = response.get(

                "result",

                {}

            ).get(

                "list",

                []

            )



            active_position = None



            for pos in positions:


                size = float(

                    pos.get(

                        "size",

                        0

                    )

                )


                if size > 0:

                    active_position = pos

                    break



            if active_position is None:

                self.clear()

                return self.current




            pos = active_position



            size = float(

                pos.get(

                    "size",

                    0

                )

            )



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

                    )

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



    # =====================================
    # CLEAR
    # =====================================

    def clear(self):


        self.current = {

            "side": None,

            "size": 0,

            "avg_price": 0,

            "unrealised_pnl": 0

        }



    # =====================================
    # GETTERS
    # =====================================

    def has_position(self):

        return self.current["size"] > 0



    def get_side(self):

        return self.current["side"]



    def get_size(self):

        return self.current["size"]



    def get_avg_price(self):

        return self.current["avg_price"]



    def get_pnl(self):

        return self.current["unrealised_pnl"]



    # =====================================
    # MONITOR
    # =====================================

    def monitor(self):


        print(
            "[POSITION MONITOR START]"
        )


        while True:


            self.sync()


            time.sleep(5)




position_manager = PositionManager()
