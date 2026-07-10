# portfolio/position_manager.py


from api.bybit_api import bybit_api



class PositionManager:


    def __init__(self):


        self.position = None



    # =====================================
    # SYNC FROM BYBIT
    # =====================================

    def sync(self):


        try:


            position = (

                bybit_api
                .get_position()

            )



            if position:


                self.position = position



                print(
                    "[POSITION SYNC]",
                    position
                )



            else:


                self.position = None



                print(
                    "[NO POSITION]"
                )



            return self.position



        except Exception as e:


            print(
                "[POSITION SYNC ERROR]",
                e
            )


            return None



    # =====================================
    # CHECK POSITION
    # =====================================

    def has_position(self):


        return (

            self.position

            is not None

        )



    # =====================================
    # GET POSITION
    # =====================================

    def get(self):


        return self.position



    # =====================================
    # SIDE
    # =====================================

    def side(self):


        if not self.position:

            return None



        return (

            self.position
            .get("side")

        )



    # =====================================
    # SIZE
    # =====================================

    def size(self):


        if not self.position:

            return 0



        return float(

            self.position
            .get(
                "size",
                0
            )

        )



    # =====================================
    # ENTRY PRICE
    # =====================================

    def entry_price(self):


        if not self.position:

            return 0



        return float(

            self.position
            .get(
                "entry_price",
                0
            )

        )



    # =====================================
    # PNL
    # =====================================

    def pnl(self):


        if not self.position:

            return 0



        return float(

            self.position
            .get(
                "unrealized_pnl",
                0
            )

        )



    # =====================================
    # UPDATE
    # =====================================

    def update(
        self,
        position
    ):


        self.position = position



    # =====================================
    # CLEAR
    # =====================================

    def clear(self):


        self.position = None



    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "has_position":

                self.has_position(),


            "side":

                self.side(),


            "size":

                self.size(),


            "entry":

                self.entry_price(),


            "pnl":

                self.pnl()


        }



# =====================================
# SINGLETON
# =====================================

position_manager = PositionManager()
