import threading


class PositionManager:


    def __init__(self):

        self.positions = {}

        self.lock = threading.Lock()



    # ==================================
    # UPDATE FROM BYBIT WS
    # ==================================

    def update_position(self, data):


        with self.lock:


            for p in data:


                symbol = p.get(
                    "symbol"
                )


                if not symbol:
                    continue



                self.positions[symbol] = {


                    "symbol":
                    symbol,


                    "side":
                    p.get("side"),


                    "size":
                    float(
                        p.get(
                            "size",
                            0
                        )
                    ),


                    "entry_price":
                    float(
                        p.get(
                            "avgPrice",
                            0
                        )
                    ),


                    "mark_price":
                    float(
                        p.get(
                            "markPrice",
                            0
                        )
                    ),


                    "unrealized_pnl":
                    float(
                        p.get(
                            "unrealisedPnl",
                            0
                        )
                    )

                }




    # ==================================
    # GET ALL
    # ==================================

    def get_positions(self):

        with self.lock:

            return list(
                self.positions.values()
            )



    # ==================================
    # GET ONE
    # ==================================

    def get_position(self, symbol):

        return self.positions.get(
            symbol
        )



position_manager = PositionManager()
