# risk/trailing_stop_manager.py

import os
import threading

from dotenv import load_dotenv


load_dotenv()





class TrailingStopManager:
    """
    Trailing Stop Manager

    기능:
    - 포지션별 최고/최저 가격 관리
    - Stop 가격 계산
    - 자동 리셋
    """



    def __init__(self):


        self.lock = threading.Lock()


        self.enabled = (

            os.getenv(

                "USE_TRAILING_STOP",

                "true"

            ).lower()

            ==

            "true"

        )


        self.percent = float(

            os.getenv(

                "TRAILING_STOP_PERCENT",

                "0.5"

            )

        )


        self.positions = {}





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

            return



        with self.lock:


            if symbol not in self.positions:


                self.positions[symbol] = {


                    "side":

                        side,


                    "high":

                        price,


                    "low":

                        price

                }


                return





            data = self.positions[symbol]



            if side == "Buy":


                if price > data["high"]:

                    data["high"] = price



            elif side == "Sell":


                if price < data["low"]:

                    data["low"] = price





    # =====================================
    # CALCULATE STOP
    # =====================================

    def calculate_stop(
        self,
        symbol,
        side
    ):


        if not self.enabled:

            return None



        with self.lock:


            data = self.positions.get(

                symbol

            )



            if not data:

                return None



            rate = (

                self.percent

                /

                100

            )





            # LONG

            if side == "Buy":


                high = data["high"]



                stop = (

                    high

                    *

                    (

                        1-rate

                    )

                )



                return round(

                    stop,

                    2

                )





            # SHORT

            if side == "Sell":


                low = data["low"]



                stop = (

                    low

                    *

                    (

                        1+rate

                    )

                )



                return round(

                    stop,

                    2

                )





            return None





    # =====================================
    # RESET
    # =====================================

    def reset(
        self,
        symbol
    ):


        with self.lock:


            if symbol in self.positions:


                del self.positions[symbol]





    # =====================================
    # CLEAR
    # =====================================

    def clear(self):


        with self.lock:


            self.positions.clear()





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        with self.lock:


            return {


                "enabled":

                    self.enabled,


                "percent":

                    self.percent,


                "positions":

                    self.positions.copy()

            }





trailing_stop_manager = TrailingStopManager()
