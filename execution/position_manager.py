from config import (
    CATEGORY,
    DEFAULT_SYMBOL,
    TAKE_PROFIT_PERCENT,
    STOP_LOSS_PERCENT,
)




# ==========================================
# POSITION MANAGER
# ==========================================

class PositionManager:


    def __init__(self):


        self.side = None

        self.entry_price = 0

        self.qty = 0



        print("==============================")
        print("[POSITION MANAGER INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")





    # ======================================
    # UPDATE POSITION
    # ======================================

    def update_position(

        self,

        side,

        qty,

        entry_price

    ):


        self.side = side

        self.qty = float(qty)

        self.entry_price = float(entry_price)



        print(
            "[POSITION UPDATED]",
            self.side,
            self.qty,
            self.entry_price
        )





    # ======================================
    # CLEAR
    # ======================================

    def clear(self):


        self.side = None

        self.qty = 0

        self.entry_price = 0



        print(
            "[POSITION CLEARED]"
        )





    # ======================================
    # CHECK POSITION
    # ======================================

    def has_position(self):


        return (

            self.side is not None

            and

            self.qty > 0

        )





    # ======================================
    # EXIT CHECK
    # ======================================

    def evaluate_exit(

        self,

        entry_price,

        side,

        closes

    ):


        try:


            if len(closes) == 0:

                return None




            current_price = float(

                closes[-1]

            )




            entry_price = float(

                entry_price

            )





            # --------------------------
            # LONG
            # --------------------------

            if side == "Buy":



                profit = (

                    (

                        current_price

                        -

                        entry_price

                    )

                    /

                    entry_price

                    *

                    100

                )




                if profit >= TAKE_PROFIT_PERCENT:


                    print(
                        "[TAKE PROFIT]",
                        round(profit,2),
                        "%"
                    )


                    return "TAKE_PROFIT"




                if profit <= -STOP_LOSS_PERCENT:


                    print(
                        "[STOP LOSS]",
                        round(profit,2),
                        "%"
                    )


                    return "STOP_LOSS"






            # --------------------------
            # SHORT
            # --------------------------

            elif side == "Sell":



                profit = (

                    (

                        entry_price

                        -

                        current_price

                    )

                    /

                    entry_price

                    *

                    100

                )





                if profit >= TAKE_PROFIT_PERCENT:


                    print(
                        "[TAKE PROFIT]",
                        round(profit,2),
                        "%"
                    )


                    return "TAKE_PROFIT"





                if profit <= -STOP_LOSS_PERCENT:


                    print(
                        "[STOP LOSS]",
                        round(profit,2),
                        "%"
                    )


                    return "STOP_LOSS"





            return None




        except Exception as e:


            print(
                "[EXIT CHECK ERROR]",
                e
            )


            return None





    # ======================================
    # GET POSITION
    # ======================================

    def get_position(self):


        return {

            "side": self.side,

            "qty": self.qty,

            "entry_price": self.entry_price

        }





# ==========================================
# SINGLETON
# ==========================================

position_manager = PositionManager()
