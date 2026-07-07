import os
from dotenv import load_dotenv


load_dotenv()



class TrailingStopManager:


    def __init__(self):

        self.enabled = (

            os.getenv(
                "TRAILING_STOP_ENABLE",
                "true"
            ).lower()
            == "true"

        )


        self.callback_percent = float(

            os.getenv(
                "TRAILING_STOP_PERCENT",
                "0.5"
            )

        )


        self.highest_price = {}

        self.lowest_price = {}



    # =====================================
    # UPDATE PRICE
    # =====================================

    def update(
        self,
        symbol,
        side,
        price
    ):


        if not self.enabled:

            return None



        price = float(price)



        # LONG

        if side.lower() == "buy":


            current_high = self.highest_price.get(

                symbol,

                0

            )



            if price > current_high:


                self.highest_price[symbol] = price



            stop_price = (

                self.highest_price[symbol]

                *

                (
                    1 -

                    self.callback_percent / 100

                )

            )



        # SHORT

        else:


            current_low = self.lowest_price.get(

                symbol,

                float("inf")

            )



            if price < current_low:


                self.lowest_price[symbol] = price



            stop_price = (

                self.lowest_price[symbol]

                *

                (
                    1 +

                    self.callback_percent / 100

                )

            )



        return round(
            stop_price,
            2
        )





    # =====================================
    # RESET POSITION
    # =====================================

    def reset(
        self,
        symbol
    ):


        self.highest_price.pop(
            symbol,
            None
        )


        self.lowest_price.pop(
            symbol,
            None
        )





trailing_stop_manager = TrailingStopManager()
