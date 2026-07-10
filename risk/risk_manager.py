import time
from datetime import datetime

from config import (
    MAX_DAILY_LOSS_PERCENT,
    MAX_POSITION_SIZE,
)


class RiskManager:


    def __init__(self):

        self.start_equity = 0.0

        self.current_equity = 0.0

        self.highest_equity = 0.0

        self.initialized = False


        self.daily_loss_limit = (
            MAX_DAILY_LOSS_PERCENT
        )


        self.max_drawdown_percent = 15.0


        self.risk_per_trade = 0.01


        self.consecutive_losses = 0


        self.max_consecutive_losses = 5


        self.kill_switch = False


        self.daily_reset_time = datetime.now().date()



    # =====================================================
    # INITIALIZE
    # =====================================================

    def initialize(self, equity):

        try:

            equity = float(equity)

            self.start_equity = equity

            self.current_equity = equity

            self.highest_equity = equity

            self.initialized = True

            self.kill_switch = False


            print(
                "[RISK INITIALIZED]",
                equity
            )


        except Exception as e:

            print(
                "[RISK INIT ERROR]",
                e
            )



    # =====================================================
    # UPDATE EQUITY
    # =====================================================

    def update_equity(self, equity):

        try:

            self.current_equity = float(equity)


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



    # =====================================================
    # DAILY RESET
    # =====================================================

    def reset_daily(self):

        today = datetime.now().date()


        if today != self.daily_reset_time:


            self.start_equity = (
                self.current_equity
            )


            self.daily_reset_time = today


            self.consecutive_losses = 0


            self.kill_switch = False


            print(
                "[RISK DAILY RESET]"
            )



    # =====================================================
    # LOSS %
    # =====================================================

    def loss_percent(self):


        if self.start_equity <= 0:

            return 0


        return (

            (
                self.start_equity
                -
                self.current_equity
            )
            /
            self.start_equity

        ) * 100



    # =====================================================
    # DRAWDOWN
    # =====================================================

    def drawdown_percent(self):


        if self.highest_equity <= 0:

            return 0


        return (

            (
                self.highest_equity
                -
                self.current_equity
            )
            /
            self.highest_equity

        ) * 100



    # =====================================================
    # TRADE PERMISSION
    # =====================================================

    def can_trade(self):


        self.reset_daily()



        if not self.initialized:

            return False



        if self.kill_switch:

            print(
                "[RISK BLOCK] KILL SWITCH"
            )

            return False



        if (

            self.loss_percent()
            >=
            self.daily_loss_limit

        ):


            self.activate_kill_switch(

                "DAILY LOSS LIMIT"

            )

            return False



        if (

            self.drawdown_percent()
            >=
            self.max_drawdown_percent

        ):


            self.activate_kill_switch(

                "MAX DRAWDOWN"

            )

            return False



        if (

            self.consecutive_losses
            >=
            self.max_consecutive_losses

        ):


            print(
                "[RISK BLOCK] LOSS STREAK"
            )


            return False



        return True



    # =====================================================
    # POSITION SIZE
    # =====================================================

    def calculate_position_size(

        self,

        entry_price,

        stop_price

    ):


        if self.current_equity <= 0:

            return 0



        risk_amount = (

            self.current_equity

            *

            self.risk_per_trade

        )



        distance = abs(

            entry_price
            -
            stop_price

        )



        if distance <= 0:

            return 0



        qty = (

            risk_amount
            /
            distance

        )



        if qty > MAX_POSITION_SIZE:

            qty = MAX_POSITION_SIZE



        return round(

            qty,

            6

        )



    # =====================================================
    # RECORD RESULT
    # =====================================================

    def record_trade(self, pnl):


        if pnl < 0:

            self.consecutive_losses += 1


        else:

            self.consecutive_losses = 0



    # =====================================================
    # KILL SWITCH
    # =====================================================

    def activate_kill_switch(self, reason):


        self.kill_switch = True


        print(
            "[KILL SWITCH]",
            reason
        )



    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "equity":

                self.current_equity,


            "daily_loss":

                self.loss_percent(),


            "drawdown":

                self.drawdown_percent(),


            "loss_streak":

                self.consecutive_losses,


            "kill":

                self.kill_switch,


            "can_trade":

                self.can_trade()

        }



risk_manager = RiskManager()
