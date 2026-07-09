import time



class RiskManager:


    def __init__(self):


        # ======================
        # SETTINGS
        # ======================


        self.max_position_size = 0.01


        self.max_daily_loss = 500


        self.max_consecutive_losses = 3



        # ======================
        # STATE
        # ======================


        self.daily_pnl = 0


        self.loss_count = 0


        self.trading_enabled = True



        self.day = time.strftime(
            "%Y-%m-%d"
        )



        print(
            "[RISK MANAGER READY]"
        )





    # ==========================
    # DAY RESET
    # ==========================


    def reset_check(self):


        today = time.strftime(
            "%Y-%m-%d"
        )



        if today != self.day:


            self.day = today


            self.daily_pnl = 0


            self.loss_count = 0


            self.trading_enabled = True



            print(
                "[RISK RESET]"
            )





    # ==========================
    # ORDER CHECK
    # ==========================


    def allow_order(
            self,
            qty
    ):


        self.reset_check()



        if not self.trading_enabled:


            print(
                "[RISK BLOCK] DISABLED"
            )


            return False





        if float(qty) > self.max_position_size:


            print(
                "[RISK BLOCK] SIZE LIMIT"
            )


            return False





        if self.daily_pnl <= -self.max_daily_loss:


            print(
                "[RISK BLOCK] DAILY LOSS LIMIT"
            )


            self.trading_enabled = False


            return False





        if self.loss_count >= self.max_consecutive_losses:


            print(
                "[RISK BLOCK] LOSS STREAK"
            )


            self.trading_enabled = False


            return False




        return True






    # ==========================
    # TRADE RESULT
    # ==========================


    def update_result(
            self,
            pnl
    ):


        pnl = float(pnl)



        self.daily_pnl += pnl



        if pnl < 0:


            self.loss_count += 1


        else:


            self.loss_count = 0





        print(
            "[RISK UPDATE]",
            {
                "daily": self.daily_pnl,
                "loss": self.loss_count
            }
        )







    # ==========================
    # EMERGENCY STOP
    # ==========================


    def emergency_stop(self):


        self.trading_enabled = False



        print(
            "[EMERGENCY STOP]"
        )






    def status(self):


        return {


            "enabled":

            self.trading_enabled,


            "daily_pnl":

            self.daily_pnl,


            "loss_count":

            self.loss_count


        }






risk_manager = RiskManager()
