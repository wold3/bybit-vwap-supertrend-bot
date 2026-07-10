from config import (
    TAKE_PROFIT_PERCENT,
    STOP_LOSS_PERCENT,
    CATEGORY,
    DEFAULT_SYMBOL,
)



# ==========================================
# POSITION MANAGER
# ==========================================

class PositionManager:


    def __init__(self):


        print("==============================")
        print("[POSITION MANAGER INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")


        self.position = None




    # ======================================
    # EXIT CHECK
    # ======================================

    def evaluate_exit(
        self,
        entry_price,
        side,
        prices
    ):


        try:


            if not prices:

                return None



            current_price = float(

                prices[-1]

            )



            entry_price = float(

                entry_price

            )




            # ==============================
            # LONG POSITION
            # ==============================

            if side == "Buy":


                profit_price = (

                    entry_price

                    *

                    (

                        1

                        +

                        TAKE_PROFIT_PERCENT / 100

                    )

                )



                stop_price = (

                    entry_price

                    *

                    (

                        1

                        -

                        STOP_LOSS_PERCENT / 100

                    )

                )




                if current_price >= profit_price:


                    return "TAKE_PROFIT"




                if current_price <= stop_price:


                    return "STOP_LOSS"





            # ==============================
            # SHORT POSITION
            # ==============================

            elif side == "Sell":



                profit_price = (

                    entry_price

                    *

                    (

                        1

                        -

                        TAKE_PROFIT_PERCENT / 100

                    )

                )



                stop_price = (

                    entry_price

                    *

                    (

                        1

                        +

                        STOP_LOSS_PERCENT / 100

                    )

                )




                if current_price <= profit_price:


                    return "TAKE_PROFIT"




                if current_price >= stop_price:


                    return "STOP_LOSS"




            return None




        except Exception as e:


            print(
                "[POSITION MANAGER ERROR]",
                e
            )


            return None





    # ======================================
    # UPDATE POSITION
    # ======================================

    def update(
        self,
        position
    ):


        self.position = position





    # ======================================
    # GET POSITION
    # ======================================

    def get_position(self):

        return self.position





# ==========================================
# SINGLETON
# ==========================================

position_manager = PositionManager()
