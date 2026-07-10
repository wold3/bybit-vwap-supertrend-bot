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

        self.qty = 0


        self.entry_price = 0



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


        try:


            self.side = side


            self.qty = float(qty)


            self.entry_price = float(entry_price)



            print("==============================")
            print("[POSITION UPDATED]")
            print("SIDE :", self.side)
            print("QTY :", self.qty)
            print("ENTRY :", self.entry_price)
            print("==============================")



        except Exception as e:


            print(
                "[POSITION UPDATE ERROR]",
                e
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
    # TP PRICE
    # ======================================

    def take_profit_price(self):


        if not self.has_position():


            return 0





        if self.side == "Buy":


            return (

                self.entry_price

                *

                (

                    1

                    +

                    TAKE_PROFIT_PERCENT / 100

                )

            )



        else:


            return (

                self.entry_price

                *

                (

                    1

                    -

                    TAKE_PROFIT_PERCENT / 100

                )

            )





    # ======================================
    # SL PRICE
    # ======================================

    def stop_loss_price(self):


        if not self.has_position():


            return 0





        if self.side == "Buy":


            return (

                self.entry_price

                *

                (

                    1

                    -

                    STOP_LOSS_PERCENT / 100

                )

            )



        else:


            return (

                self.entry_price

                *

                (

                    1

                    +

                    STOP_LOSS_PERCENT / 100

                )

            )





    # ======================================
    # EXIT CHECK
    # ======================================

    def check_exit(

        self,

        current_price

    ):


        if not self.has_position():


            return None





        tp = self.take_profit_price()


        sl = self.stop_loss_price()





        # LONG

        if self.side == "Buy":



            if current_price >= tp:


                return "TAKE_PROFIT"




            if current_price <= sl:


                return "STOP_LOSS"






        # SHORT

        elif self.side == "Sell":



            if current_price <= tp:


                return "TAKE_PROFIT"




            if current_price >= sl:


                return "STOP_LOSS"





        return None





    # ======================================
    # STATUS
    # ======================================

    def status(self):


        return {


            "side":

                self.side,


            "qty":

                self.qty,


            "entry":

                self.entry_price,


            "tp":

                self.take_profit_price(),


            "sl":

                self.stop_loss_price()

        }





# ==========================================
# SINGLETON
# ==========================================

position_manager = PositionManager()
