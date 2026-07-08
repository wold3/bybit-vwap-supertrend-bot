import os
import threading

from dotenv import load_dotenv


load_dotenv()



class DrawdownGuard:
    """
    Drawdown Guard

    기능:
    - 최고 Equity 기록
    - 현재 Drawdown 계산
    - 최대 손실 초과 시 거래 차단
    """



    def __init__(self):

        self.lock = threading.Lock()



        self.max_drawdown = float(

            os.getenv(

                "MAX_DAILY_LOSS",

                "-50"

            )

        )



        self.peak_equity = None

        self.current_equity = None

        self.current_drawdown = 0.0





    # =====================================
    # EQUITY UPDATE
    # =====================================

    def update(
        self,
        equity
    ):


        with self.lock:


            equity = float(equity)


            self.current_equity = equity



            if self.peak_equity is None:


                self.peak_equity = equity



            if equity > self.peak_equity:


                self.peak_equity = equity



            self.current_drawdown = (

                equity

                -

                self.peak_equity

            )



            return self.current_drawdown





    # =====================================
    # TRADE ALLOWED?
    # =====================================

    def can_trade(
        self
    ):


        with self.lock:


            return (

                self.current_drawdown

                >

                self.max_drawdown

            )





    # =====================================
    # SHOULD STOP
    # =====================================

    def is_triggered(
        self
    ):


        with self.lock:


            return (

                self.current_drawdown

                <=

                self.max_drawdown

            )





    # =====================================
    # RESET
    # =====================================

    def reset(
        self
    ):


        with self.lock:


            self.peak_equity = None

            self.current_equity = None

            self.current_drawdown = 0.0





    # =====================================
    # STATUS
    # =====================================

    def status(
        self
    ):


        with self.lock:


            return {


                "peak_equity":

                    self.peak_equity,


                "current_equity":

                    self.current_equity,


                "drawdown":

                    self.current_drawdown,


                "max_drawdown":

                    self.max_drawdown,


                "can_trade":

                    self.current_drawdown > self.max_drawdown

            }





# singleton

drawdown_guard = DrawdownGuard()
