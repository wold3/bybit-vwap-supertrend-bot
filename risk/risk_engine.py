# risk/risk_engine.py

import os
import time
import threading

from dotenv import load_dotenv


load_dotenv()



class RiskEngine:
    """
    Risk Management Engine

    기능:
    - 최대 거래 횟수 제한
    - 일일 거래 관리
    - 거래 상태 확인
    """



    def __init__(self):


        self.lock = threading.Lock()


        self.max_trades = int(

            os.getenv(

                "MAX_TRADES",

                "100"

            )

        )


        self.trade_count = 0


        self.day_start = self.get_day()





    # =====================================
    # DAY
    # =====================================

    def get_day(self):


        return time.strftime(

            "%Y-%m-%d"

        )





    # =====================================
    # RESET CHECK
    # =====================================

    def check_daily_reset(self):


        today = self.get_day()



        if today != self.day_start:


            self.trade_count = 0


            self.day_start = today





    # =====================================
    # CAN TRADE
    # =====================================

    def can_trade(self):


        with self.lock:


            self.check_daily_reset()



            return (

                self.trade_count

                <

                self.max_trades

            )





    # =====================================
    # REGISTER TRADE
    # =====================================

    def register_trade(self):


        with self.lock:


            self.check_daily_reset()



            self.trade_count += 1



            return self.trade_count





    # =====================================
    # REMAINING
    # =====================================

    def remaining_trades(self):


        with self.lock:


            self.check_daily_reset()



            return max(

                self.max_trades

                -

                self.trade_count,

                0

            )





    # =====================================
    # RESET
    # =====================================

    def reset(self):


        with self.lock:


            self.trade_count = 0


            self.day_start = self.get_day()





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        with self.lock:


            self.check_daily_reset()



            return {


                "trade_count":

                    self.trade_count,


                "max_trades":

                    self.max_trades,


                "remaining":

                    self.remaining_trades(),


                "day":

                    self.day_start,


                "can_trade":

                    self.trade_count

                    <

                    self.max_trades

            }





risk_engine = RiskEngine()
