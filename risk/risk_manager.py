# =====================================================
# risk/risk_manager.py
# VWAP SUPERTREND BOT RISK MANAGER
# =====================================================

import threading
import datetime


from config import (

    RISK_PERCENT,

    MAX_POSITION_SIZE

)


from web.server import (

    update_status,

    add_log

)





class RiskManager:


    def __init__(self):


        self.lock = threading.RLock()


        self.enabled = True


        self.kill_switch = False


        self.daily_pnl = 0.0


        self.loss_count = 0



        # risk limit

        self.max_daily_loss = -5.0


        self.max_loss_count = 5



        self.today = datetime.date.today()



        print(

            "[RISK MANAGER READY]"

        )





    # =====================================================
    # DAILY RESET CHECK
    # =====================================================

    def reset_check(self):


        today = datetime.date.today()



        if today != self.today:


            self.today = today


            self.daily_pnl = 0.0


            self.loss_count = 0


            self.kill_switch = False



            add_log(

                "RISK DAILY RESET"

            )


            update_status({

                "daily_pnl":0,

                "loss_count":0,

                "kill_switch":False

            })





    # =====================================================
    # ORDER PERMISSION
    # =====================================================

    def allow_order(self, qty):


        with self.lock:


            self.reset_check()



            if not self.enabled:


                add_log(

                    "RISK DISABLED"

                )

                return False




            if self.kill_switch:


                add_log(

                    "KILL SWITCH ACTIVE"

                )

                return False





            try:


                qty = float(qty)


            except Exception:


                add_log(

                    "INVALID QTY"

                )

                return False





            if qty <= 0:


                add_log(

                    "ZERO QTY BLOCK"

                )

                return False





            if qty > MAX_POSITION_SIZE:


                add_log(

                    "MAX POSITION LIMIT"

                )

                return False





            if self.daily_pnl <= self.max_daily_loss:


                self.activate_kill(

                    "DAILY LOSS LIMIT"

                )

                return False





            if self.loss_count >= self.max_loss_count:


                self.activate_kill(

                    "LOSS COUNT LIMIT"

                )

                return False





            return True





    # =====================================================
    # UPDATE PNL
    # =====================================================

    def update_pnl(self, pnl):


        with self.lock:


            try:


                pnl = float(pnl)


            except Exception:


                return False





            self.daily_pnl += pnl





            if pnl < 0:


                self.loss_count += 1





            update_status({

                "daily_pnl":

                    self.daily_pnl,


                "loss_count":

                    self.loss_count


            })



            # 자동 보호

            if self.daily_pnl <= self.max_daily_loss:


                self.activate_kill(

                    "AUTO DAILY LOSS"

                )



            if self.loss_count >= self.max_loss_count:


                self.activate_kill(

                    "AUTO LOSS COUNT"

                )



            return True





    # =====================================================
    # KILL SWITCH
    # =====================================================

    def activate_kill(self, reason):


        self.kill_switch = True



        add_log(

            f"KILL SWITCH : {reason}"

        )



        update_status({

            "bot":

                "KILLED",


            "kill_switch":

                True

        })





    # =====================================================
    # RESET KILL
    # =====================================================

    def reset_kill(self):


        with self.lock:


            self.kill_switch = False



            add_log(

                "KILL SWITCH RESET"

            )



            update_status({

                "kill_switch":

                    False

            })





    # =====================================================
    # ENABLE
    # =====================================================

    def enable(self):


        with self.lock:


            self.enabled = True


            add_log(

                "RISK ENABLE"

            )





    # =====================================================
    # DISABLE
    # =====================================================

    def disable(self):


        with self.lock:


            self.enabled = False


            add_log(

                "RISK DISABLE"

            )





    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        with self.lock:


            return {


                "enabled":

                    self.enabled,


                "kill_switch":

                    self.kill_switch,


                "risk_percent":

                    RISK_PERCENT,


                "daily_pnl":

                    self.daily_pnl,


                "loss_count":

                    self.loss_count


            }





# =====================================================
# INSTANCE
# =====================================================

risk_manager = RiskManager()
