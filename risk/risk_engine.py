import os
import threading

from dotenv import load_dotenv


load_dotenv()



class RiskEngine:
    """
    Risk Engine

    기능:
    - 최대 거래 횟수 제한
    - 최대 동시 포지션 제한
    - 일일 손실 제한
    - 거래 기록 관리
    - 거래 가능 여부 판단
    """



    def __init__(self):

        self.lock = threading.Lock()



        # =====================================
        # CONFIG
        # =====================================

        self.max_trades = int(

            os.getenv(

                "MAX_TRADES",

                "100"

            )

        )



        self.max_positions = int(

            os.getenv(

                "MAX_POSITIONS",

                "3"

            )

        )



        self.max_daily_loss = float(

            os.getenv(

                "MAX_DAILY_LOSS",

                "100"

            )

        )



        # =====================================
        # STATE
        # =====================================

        self.trade_count = 0

        self.open_positions = 0

        self.daily_pnl = 0.0



    # =====================================
    # CAN TRADE
    # =====================================

    def can_trade(
        self
    ):

        with self.lock:


            if self.trade_count >= self.max_trades:

                return False



            if self.open_positions >= self.max_positions:

                return False



            if self.daily_pnl <= -abs(
                self.max_daily_loss
            ):

                return False



            return True



    # =====================================
    # REGISTER ENTRY
    # =====================================

    def register_trade(
        self
    ):

        with self.lock:


            self.trade_count += 1

            self.open_positions += 1



    # =====================================
    # CLOSE TRADE
    # =====================================

    def close_trade(
        self,
        pnl=0
    ):

        with self.lock:


            if self.open_positions > 0:

                self.open_positions -= 1



            self.daily_pnl += float(
                pnl
            )



    # =====================================
    # UPDATE PNL
    # =====================================

    def update_pnl(
        self,
        pnl
    ):

        with self.lock:


            self.daily_pnl += float(
                pnl
            )



    # =====================================
    # RESET DAILY
    # =====================================

    def reset(
        self
    ):

        with self.lock:


            self.trade_count = 0

            self.open_positions = 0

            self.daily_pnl = 0.0



    # =====================================
    # FORCE STOP
    # =====================================

    def emergency_stop(
        self
    ):

        with self.lock:


            self.daily_pnl = -abs(
                self.max_daily_loss
            )



    # =====================================
    # STATUS
    # =====================================

    def status(
        self
    ):

        with self.lock:


            return {


                "trade_count":

                    self.trade_count,


                "max_trades":

                    self.max_trades,


                "open_positions":

                    self.open_positions,


                "max_positions":

                    self.max_positions,


                "daily_pnl":

                    self.daily_pnl,


                "max_daily_loss":

                    self.max_daily_loss,


                "can_trade":

                    (

                        self.trade_count < self.max_trades

                        and

                        self.open_positions < self.max_positions

                        and

                        self.daily_pnl > -abs(
                            self.max_daily_loss
                        )

                    )

            }





# =====================================
# SINGLETON
# =====================================

risk_engine = RiskEngine()
