import numpy as np

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

        print("==============================")
        print("[POSITION MANAGER INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")


    # ======================================
    # TP / SL PRICE
    # ======================================

    def calculate_exit_price(
        self,
        entry_price,
        side
    ):


        try:


            entry_price = float(
                entry_price
            )



            if side == "Buy":


                tp = entry_price * (

                    1
                    +
                    TAKE_PROFIT_PERCENT / 100

                )


                sl = entry_price * (

                    1
                    -
                    STOP_LOSS_PERCENT / 100

                )



            elif side == "Sell":


                tp = entry_price * (

                    1
                    -
                    TAKE_PROFIT_PERCENT / 100

                )


                sl = entry_price * (

                    1
                    +
                    STOP_LOSS_PERCENT / 100

                )


            else:

                return None, None



            return tp, sl



        except Exception as e:


            print(
                "[EXIT PRICE ERROR]",
                e
            )


            return None, None




    # ======================================
    # ATR LEVEL
    # ======================================

    def calc_atr_levels(
        self,
        prices,
        period=20,
        multiplier=2
    ):


        if len(prices) < period:

            return None, None



        high = max(
            prices[-period:]
        )


        low = min(
            prices[-period:]
        )


        atr = (

            high - low

        ) / period



        return (

            atr * multiplier,

            atr * multiplier

        )




    # ======================================
    # STOP LOSS CHECK
    # ======================================

    def should_stop_loss(
        self,
        entry_price,
        current_price,
        side,
        sl
    ):


        if side == "Buy":

            return (

                current_price
                <=
                entry_price - sl

            )



        if side == "Sell":

            return (

                current_price
                >=
                entry_price + sl

            )



        return False




    # ======================================
    # TAKE PROFIT CHECK
    # ======================================

    def should_take_profit(
        self,
        entry_price,
        current_price,
        side,
        tp
    ):


        if side == "Buy":

            return (

                current_price
                >=
                entry_price + tp

            )



        if side == "Sell":

            return (

                current_price
                <=
                entry_price - tp

            )



        return False




    # ======================================
    # EXIT SIGNAL
    # ======================================

    def evaluate_exit(
        self,
        entry_price,
        side,
        prices
    ):


        try:


            current_price = prices[-1]



            tp, sl = self.calc_atr_levels(

                prices

            )



            if tp is None:

                return None



            if self.should_stop_loss(

                entry_price,

                current_price,

                side,

                sl

            ):


                return "STOP_LOSS"




            if self.should_take_profit(

                entry_price,

                current_price,

                side,

                tp

            ):


                return "TAKE_PROFIT"




            return None




        except Exception as e:


            print(
                "[EXIT ERROR]",
                e
            )


            return None




# ==========================================
# SINGLETON
# ==========================================

position_manager = PositionManager()
