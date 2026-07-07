import os
import time
import threading

from dotenv import load_dotenv


load_dotenv()





class DrawdownGuard:


    def __init__(self):


        self.max_drawdown = float(

            os.getenv(

                "MAX_DRAWDOWN",

                "10"

            )

        )



        self.current_equity = 0


        self.peak_equity = 0


        self.drawdown = 0



        self.history = []



        self.block_trade = False



        self.lock = threading.Lock()





    # =====================================
    # UPDATE EQUITY
    # =====================================

    def update(
        self,
        equity
    ):


        with self.lock:


            equity = float(
                equity
            )


            self.current_equity = equity



            # 최고 자산 갱신

            if equity > self.peak_equity:


                self.peak_equity = equity





            if self.peak_equity > 0:


                self.drawdown = (

                    (

                        self.peak_equity

                        -

                        equity

                    )

                    /

                    self.peak_equity

                )

                *

                100



            else:


                self.drawdown = 0





            # 기록

            self.history.append({


                "time":

                    time.time(),


                "equity":

                    equity,


                "drawdown":

                    round(

                        self.drawdown,

                        2

                    )

            })



            # 최근 1000개 유지

            if len(self.history) > 1000:


                self.history.pop(0)





            # 위험 차단

            if self.drawdown >= self.max_drawdown:


                self.block_trade = True



                print(

                    "🚨 MAX DRAWDOWN REACHED",

                    self.drawdown

                )





    # =====================================
    # TRADE CHECK
    # =====================================

    def can_trade(
        self
    ):


        with self.lock:


            return not self.block_trade





    # =====================================
    # RESET
    # =====================================

    def reset(
        self
    ):


        with self.lock:


            self.block_trade = False


            self.drawdown = 0





    # =====================================
    # HISTORY
    # =====================================

    def get_history(
        self
    ):


        with self.lock:


            return self.history





    # =====================================
    # STATUS
    # =====================================

    def status(
        self
    ):


        with self.lock:


            return {


                "current_equity":

                    self.current_equity,


                "peak_equity":

                    self.peak_equity,


                "drawdown":

                    round(

                        self.drawdown,

                        2

                    ),


                "max_drawdown":

                    self.max_drawdown,


                "can_trade":

                    not self.block_trade

            }





drawdown_guard = DrawdownGuard()
