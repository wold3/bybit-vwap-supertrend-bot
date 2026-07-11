# =====================================================
# risk/risk_manager.py
# VWAP SUPERTREND BOT
# RISK MANAGER
# =====================================================


import time



from config import (

    MAX_POSITION_SIZE,

    MAX_DAILY_LOSS,

    MAX_OPEN_POSITION

)



from web.server import (

    add_log,

    update_status

)





class RiskManager:



    def __init__(self):


        self.daily_loss = 0


        self.order_count = 0


        self.last_reset = time.time()



        print(

            "[RISK MANAGER READY]"

        )









    # =====================================================
    # DAILY RESET
    # =====================================================

    def reset_check(self):


        now = time.time()



        # 24시간 초기화

        if now - self.last_reset > 86400:


            self.daily_loss = 0


            self.order_count = 0


            self.last_reset = now



            add_log(

                "RISK DAILY RESET"

            )








    # =====================================================
    # ORDER CHECK
    # =====================================================

    def allow_order(self, qty):


        try:


            self.reset_check()






            qty = float(qty)





            # 수량 제한

            if qty > MAX_POSITION_SIZE:


                add_log(

                    f"RISK BLOCK SIZE {qty}"

                )


                return False







            # 포지션 개수 제한

            if self.order_count >= MAX_OPEN_POSITION:


                add_log(

                    "RISK BLOCK MAX POSITION"

                )


                return False






            # 손실 제한

            if self.daily_loss >= MAX_DAILY_LOSS:


                add_log(

                    "RISK BLOCK DAILY LOSS"

                )


                return False








            self.order_count += 1



            update_status({


                "risk":

                    "OK",


                "order_count":

                    self.order_count


            })



            return True






        except Exception as e:


            add_log(

                f"RISK ERROR {e}"

            )


            return False









    # =====================================================
    # PNL UPDATE
    # =====================================================

    def update_pnl(self, pnl):


        try:


            pnl=float(pnl)



            if pnl < 0:


                self.daily_loss += abs(pnl)





            update_status({


                "daily_loss":

                    self.daily_loss


            })




        except Exception as e:


            add_log(

                f"PNL UPDATE ERROR {e}"

            )








    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "daily_loss":

                self.daily_loss,


            "order_count":

                self.order_count

        }








    # =====================================================
    # RESET
    # =====================================================

    def reset(self):


        self.daily_loss = 0


        self.order_count = 0


        add_log(

            "RISK RESET"

        )







# =====================================================
# INSTANCE
# =====================================================

risk_manager = RiskManager()
