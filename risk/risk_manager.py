# risk/risk_manager.py


import time


from config import (
    MAX_DAILY_LOSS_PERCENT,
    MAX_POSITION_SIZE,
)



class RiskManager:


    def __init__(self):


        self.start_equity = 0

        self.current_equity = 0

        self.highest_equity = 0


        self.initialized = False


        self.trading_enabled = True


        self.daily_loss_limit = (
            MAX_DAILY_LOSS_PERCENT
        )


        self.loss_streak = 0


        self.max_loss_streak = 5



        print(
            "[RISK MANAGER INIT]"
        )



    # =====================================
    # INITIALIZE
    # =====================================

    def initialize(
        self,
        equity
    ):


        try:


            equity = float(equity)


            self.start_equity = equity

            self.current_equity = equity

            self.highest_equity = equity


            self.initialized = True


            self.trading_enabled = True



            print(
                "[RISK READY]",
                equity
            )



        except Exception as e:


            print(
                "[RISK INIT ERROR]",
                e
            )



    # =====================================
    # UPDATE EQUITY
    # =====================================

    def update_equity(
        self,
        equity
    ):


        try:


            self.current_equity = float(
                equity
            )


            if (
                self.current_equity
                >
                self.highest_equity
            ):

                self.highest_equity = (
                    self.current_equity
                )



        except:


            pass




    # =====================================
    # DAILY LOSS
    # =====================================

    def loss_percent(self):


        if self.start_equity <= 0:

            return 0



        loss = (

            self.start_equity

            -

            self.current_equity

        )


        return (

            loss /

            self.start_equity

        ) * 100




    # =====================================
    # DRAWDOWN
    # =====================================

    def drawdown_percent(self):


        if self.highest_equity <= 0:

            return 0



        dd = (

            self.highest_equity

            -

            self.current_equity

        )


        return (

            dd /

            self.highest_equity

        ) * 100




    # =====================================
    # TRADE CHECK
    # =====================================

    def can_trade(self):


        if not self.initialized:


            print(
                "[RISK BLOCK] NOT INIT"
            )


            return False



        if not self.trading_enabled:


            print(
                "[RISK BLOCK] KILL SWITCH"
            )


            return False




        if (
            self.loss_percent()
            >=
            self.daily_loss_limit
        ):


            print(
                "[DAILY LOSS LIMIT]"
            )


            self.emergency_stop()


            return False




        if self.loss_streak >= self.max_loss_streak:


            print(
                "[LOSS STREAK BLOCK]"
            )


            return False



        return True




    # =====================================
    # POSITION SIZE
    # =====================================

    def check_position_size(
        self,
        qty
    ):


        try:


            qty = float(qty)



            if qty > MAX_POSITION_SIZE:


                print(
                    "[POSITION TOO LARGE]"
                )


                return False



            return True



        except:


            return False




    # =====================================
    # ATR POSITION SIZE
    # =====================================

    def calculate_position_size(
        self,
        risk_percent,
        stop_distance
    ):


        if self.current_equity <= 0:

            return 0



        if stop_distance <= 0:

            return 0



        risk_amount = (

            self.current_equity

            *

            risk_percent

            /

            100

        )



        qty = (

            risk_amount

            /

            stop_distance

        )


        return qty




    # =====================================
    # TRADE RESULT
    # =====================================

    def record_trade(
        self,
        pnl
    ):


        if pnl < 0:


            self.loss_streak += 1


        else:


            self.loss_streak = 0




    # =====================================
    # KILL SWITCH
    # =====================================

    def emergency_stop(self):


        self.trading_enabled = False


        print(
            "================="
        )

        print(
            "[KILL SWITCH]"
        )

        print(
            "NEW ORDERS BLOCKED"
        )

        print(
            "================="
        )



    # =====================================
    # RESET
    # =====================================

    def reset(self):


        self.trading_enabled = True

        self.loss_streak = 0



    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "equity":

                self.current_equity,


            "loss":

                self.loss_percent(),


            "drawdown":

                self.drawdown_percent(),


            "loss_streak":

                self.loss_streak,


            "enabled":

                self.trading_enabled

        }




risk_manager = RiskManager()
