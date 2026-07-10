# risk/risk_manager.py


import time



from config import (

    MAX_DAILY_LOSS_PERCENT,

    MAX_POSITION_SIZE,

    MAX_DRAWDOWN_PERCENT,

    MAX_LOSS_STREAK,

    ORDER_COOLDOWN,

    RISK_PER_TRADE_PERCENT

)





class RiskManager:



    def __init__(self):


        self.start_equity = 0


        self.current_equity = 0


        self.highest_equity = 0



        self.initialized = False



        self.kill_switch = False



        self.loss_streak = 0



        self.last_trade_time = 0



        self.daily_loss_limit = (

            MAX_DAILY_LOSS_PERCENT

        )



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


        self.start_equity = float(

            equity

        )


        self.current_equity = float(

            equity

        )


        self.highest_equity = float(

            equity

        )


        self.initialized = True



        self.kill_switch = False



        print(

            "[RISK READY]",

            equity

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


            if self.current_equity > self.highest_equity:


                self.highest_equity = self.current_equity



        except:


            pass







    # =====================================
    # DAILY LOSS
    # =====================================

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






    # =====================================
    # DRAWDOWN
    # =====================================

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






    # =====================================
    # TRADE PERMISSION
    # =====================================

    def can_trade(self):


        if not self.initialized:


            return False




        if self.kill_switch:


            print(

                "[RISK BLOCK] KILL SWITCH"

            )


            return False





        if self.loss_percent() >= self.daily_loss_limit:


            print(

                "[RISK BLOCK] DAILY LOSS"

            )


            self.emergency_stop()



            return False






        if self.drawdown_percent() >= MAX_DRAWDOWN_PERCENT:


            print(

                "[RISK BLOCK] DRAWDOWN"

            )


            self.emergency_stop()



            return False






        if self.loss_streak >= MAX_LOSS_STREAK:


            print(

                "[RISK BLOCK] LOSS STREAK"

            )


            return False






        if not self.cooldown_ok():


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


            if float(qty) > MAX_POSITION_SIZE:


                return False



            return True



        except:


            return False






    # =====================================
    # ATR POSITION SIZE
    # =====================================

    def calculate_position_size(
        self,
        entry,
        stop
    ):


        try:


            risk_amount = (

                self.current_equity

                *

                RISK_PER_TRADE_PERCENT

                /

                100

            )



            distance = abs(

                entry

                -

                stop

            )



            if distance == 0:


                return 0



            qty = (

                risk_amount

                /

                distance

            )



            return qty




        except:


            return 0







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



        self.last_trade_time = time.time()







    # =====================================
    # COOLDOWN
    # =====================================

    def cooldown_ok(self):


        if self.last_trade_time == 0:


            return True



        return (

            time.time()

            -

            self.last_trade_time

        ) >= ORDER_COOLDOWN






    # =====================================
    # KILL SWITCH
    # =====================================

    def emergency_stop(self):


        print(

            "[KILL SWITCH ON]"

        )


        self.kill_switch = True







    # =====================================
    # RESET
    # =====================================

    def reset(self):


        self.kill_switch = False


        self.loss_streak = 0


        print(

            "[RISK RESET]"

        )







    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "equity":

            self.current_equity,


            "loss_percent":

            round(

                self.loss_percent(),

                2

            ),



            "drawdown":

            round(

                self.drawdown_percent(),

                2

            ),



            "loss_streak":

            self.loss_streak,



            "kill_switch":

            self.kill_switch,



            "can_trade":

            self.can_trade()

        }







risk_manager = RiskManager()
