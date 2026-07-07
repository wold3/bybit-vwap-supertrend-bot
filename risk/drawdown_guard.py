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


        self.current_equity = 0.0


        self.peak_equity = 0.0


        self.drawdown = 0.0


        self.history = []


        self.block_trade = False


        self.lock = threading.Lock()





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



            # 최초 Equity

            if self.peak_equity == 0:


                self.peak_equity = equity





            # 최고 Equity 갱신

            if equity > self.peak_equity:


                self.peak_equity = equity





            # Drawdown 계산

            if self.peak_equity > 0:


                self.drawdown = (

                    (

                        self.peak_equity

                        -

                        equity

                    )

                    /

                    self.peak_equity

                ) * 100



            else:


                self.drawdown = 0.0





            # Equity 기록

            self.history.append({


                "time":

                    time.time(),


                "equity":

                    round(

                        equity,

                        4

                    ),


                "drawdown":

                    round(

                        self.drawdown,

                        2

                    )

            })





            # 최대 기록 제한

            if len(self.history) > 1000:


                self.history.pop(0)





            # 거래 차단

            if self.drawdown >= self.max_drawdown:


                self.block_trade = True


                print(

                    "🚨 MAX DRAWDOWN BLOCK",

                    round(

                        self.drawdown,

                        2

                    ),

                    "%"

                )





    # =====================================
    # CAN TRADE
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


            self.drawdown = 0.0


            self.history.clear()





    # =====================================
    # EQUITY HISTORY
    # Dashboard Chart
    # =====================================

    def get_history(
        self
    ):


        with self.lock:


            return list(

                self.history

            )





    # =====================================
    # STATUS
    # Dashboard Risk API
    # =====================================

    def status(
        self
    ):


        with self.lock:


            return {


                "current_equity":

                    round(

                        self.current_equity,

                        4

                    ),


                "peak_equity":

                    round(

                        self.peak_equity,

                        4

                    ),


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





    # =====================================
    # FORCE BLOCK
    # =====================================

    def block(
        self
    ):


        with self.lock:


            self.block_trade = True





    # =====================================
    # UNBLOCK
    # =====================================

    def unblock(
        self
    ):


        with self.lock:


            self.block_trade = False





drawdown_guard = DrawdownGuard()
