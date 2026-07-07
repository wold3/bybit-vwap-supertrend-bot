import threading



class PositionManager:


    def __init__(self):


        self.positions = {}


        self.lock = threading.Lock()





    # =====================================
    # BYBIT POSITION UPDATE
    # =====================================

    def update_position(
        self,
        positions
    ):


        with self.lock:


            for p in positions:


                symbol = p.get(
                    "symbol"
                )


                if not symbol:

                    continue



                size = float(

                    p.get(
                        "size",
                        0
                    )

                )



                # 포지션 종료

                if size == 0:


                    self.positions.pop(

                        symbol,

                        None

                    )


                    continue





                self.positions[symbol] = {


                    "symbol":

                        symbol,


                    "side":

                        p.get(

                            "side"

                        ),


                    "size":

                        size,


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





    # =====================================
    # SINGLE POSITION
    # =====================================

    def get_position(
        self,
        symbol
    ):


        with self.lock:


            return (

                self.positions
                .get(symbol)

            )





    # =====================================
    # ALL POSITION
    # =====================================

    def get_positions(
        self
    ):


        with self.lock:


            return list(

                self.positions.values()

            )





    # =====================================
    # CHECK HOLDING
    # =====================================

    def has_position(
        self,
        symbol
    ):


        with self.lock:


            return (

                symbol

                in

                self.positions

            )





    # =====================================
    # POSITION SIDE
    # =====================================

    def get_side(
        self,
        symbol
    ):


        position = self.get_position(

            symbol

        )


        if position:


            return position.get(

                "side"

            )


        return None





    # =====================================
    # SIZE
    # =====================================

    def get_size(
        self,
        symbol
    ):


        position = self.get_position(

            symbol

        )


        if position:


            return position.get(

                "size",

                0

            )


        return 0





position_manager = PositionManager()
