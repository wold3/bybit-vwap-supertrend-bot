import os
from dotenv import load_dotenv


load_dotenv()



class SLTPManager:


    def __init__(self):

        self.stop_loss_percent = float(

            os.getenv(
                "STOP_LOSS_PERCENT",
                "1"
            )

        )


        self.take_profit_percent = float(

            os.getenv(
                "TAKE_PROFIT_PERCENT",
                "2"
            )

        )



    # =====================================
    # SL / TP CALCULATE
    # =====================================

    def calculate(
        self,
        side,
        entry_price
    ):


        entry_price = float(
            entry_price
        )



        if side.lower() == "buy":


            stop_loss = (

                entry_price

                *

                (
                    1 -
                    self.stop_loss_percent / 100
                )

            )


            take_profit = (

                entry_price

                *

                (
                    1 +
                    self.take_profit_percent / 100
                )

            )



        else:


            stop_loss = (

                entry_price

                *

                (
                    1 +
                    self.stop_loss_percent / 100
                )

            )


            take_profit = (

                entry_price

                *

                (
                    1 -
                    self.take_profit_percent / 100
                )

            )



        return {


            "stop_loss":

                round(
                    stop_loss,
                    2
                ),



            "take_profit":

                round(
                    take_profit,
                    2
                )

        }





    # =====================================
    # TRAILING STOP PRICE
    # =====================================

    def trailing_stop(
        self,
        side,
        current_price,
        callback_percent=0.5
    ):



        if side.lower() == "buy":


            return round(

                current_price
                *
                (
                    1 -
                    callback_percent / 100
                ),

                2

            )


        else:


            return round(

                current_price
                *
                (
                    1 +
                    callback_percent / 100
                ),

                2

            )





sltp_manager = SLTPManager()
