import os
import threading

from dotenv import load_dotenv


load_dotenv()



class TrailingStopManager:


    def __init__(self):


        self.trailing_percent = float(

            os.getenv(

                "TRAILING_STOP_PERCENT",

                "1.5"

            )

        )


        # symbol별 최고/최저 가격

        self.highest_price = {}


        self.lowest_price = {}



        self.lock = threading.Lock()





    # =====================================
    # UPDATE POSITION PRICE
    # =====================================

    def update(
        self,
        symbol,
        side,
        price
    ):


        with self.lock:


            price = float(price)



            if side == "Buy":


                old = self.highest_price.get(

                    symbol,

                    price

                )



                if price > old:


                    self.highest_price[symbol] = price



            elif side == "Sell":


                old = self.lowest_price.get(

                    symbol,

                    price

                )



                if price < old:


                    self.lowest_price[symbol] = price





    # =====================================
    # CALCULATE NEW SL
    # =====================================

    def calculate_stop(
        self,
        symbol,
        side
    ):


        with self.lock:



            percent = (

                self.trailing_percent

                /

                100

            )



            # LONG

            if side == "Buy":


                highest = self.highest_price.get(

                    symbol

                )



                if not highest:


                    return None



                stop = highest * (

                    1 - percent

                )



                return round(

                    stop,

                    2

                )





            # SHORT

            elif side == "Sell":


                lowest = self.lowest_price.get(

                    symbol

                )



                if not lowest:


                    return None



                stop = lowest * (

                    1 + percent

                )



                return round(

                    stop,

                    2

                )



        return None





    # =====================================
    # SHOULD MOVE SL
    # =====================================

    def should_update(
        self,
        symbol,
        side,
        current_sl
    ):


        new_sl = self.calculate_stop(

            symbol,

            side

        )



        if not new_sl:


            return False





        current_sl = float(

            current_sl

        )



        # LONG SL 상승만 허용

        if side == "Buy":


            return new_sl > current_sl





        # SHORT SL 하락만 허용

        if side == "Sell":


            return new_sl < current_sl



        return False





    # =====================================
    # RESET
    # =====================================

    def reset(
        self,
        symbol
    ):


        with self.lock:


            self.highest_price.pop(

                symbol,

                None

            )


            self.lowest_price.pop(

                symbol,

                None

            )



            print(

                "TRAILING RESET",

                symbol

            )





    # =====================================
    # STATUS
    # =====================================

    def status(
        self
    ):


        with self.lock:


            return {


                "highest":

                    self.highest_price,


                "lowest":

                    self.lowest_price


            }





trailing_stop_manager = TrailingStopManager()
