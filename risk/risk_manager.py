# =====================================================
# risk/risk_manager.py
# VWAP SUPERTREND BOT
# ADVANCED RISK MANAGER
# =====================================================


import time
import threading



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


        self.lock = threading.Lock()



        self.daily_loss = 0


        self.order_count = 0


        self.win_count = 0


        self.loss_count = 0



        self.last_order_time = 0



        self.cooldown = 60



        self.blocked = False



        self.last_reset = time.time()



        print(

            "[RISK MANAGER READY]"

        )









    # =====================================================
    # DAILY RESET
    # =====================================================

    def reset_check(self):


        now=time.time()



        if now-self.last_reset > 86400:



            with self.lock:


                self.daily_loss=0

                self.order_count=0

                self.win_count=0

                self.loss_count=0

                self.blocked=False


                self.last_reset=now




            add_log(

                "RISK DAILY RESET"

            )









    # =====================================================
    # ORDER CHECK
    # =====================================================

    def allow_order(self,qty):


        try:



            self.reset_check()



            with self.lock:



                if self.blocked:


                    add_log(

                        "RISK BLOCKED"

                    )


                    return False





                qty=float(qty)






                # 수량 제한

                if qty > MAX_POSITION_SIZE:


                    add_log(

                        f"SIZE LIMIT {qty}"

                    )


                    return False







                # 최대 주문 제한

                if self.order_count >= MAX_OPEN_POSITION:



                    add_log(

                        "MAX POSITION LIMIT"

                    )


                    return False








                # 일손실 제한

                if self.daily_loss >= MAX_DAILY_LOSS:



                    self.blocked=True



                    add_log(

                        "DAILY LOSS STOP"

                    )



                    return False








                # 주문 간격

                if (

                    time.time()

                    -

                    self.last_order_time

                    <

                    self.cooldown

                ):



                    add_log(

                        "RISK COOLDOWN"

                    )


                    return False








                self.order_count +=1


                self.last_order_time=time.time()






            update_status({

                "risk":

                "OK",


                "orders":

                self.order_count,


                "daily_loss":

                self.daily_loss

            })




            return True





        except Exception as e:



            add_log(

                f"RISK ERROR {e}"

            )


            return False










    # =====================================================
    # PNL TRACKING
    # =====================================================

    def update_pnl(self,pnl):


        try:


            pnl=float(pnl)





            with self.lock:



                if pnl < 0:


                    self.daily_loss += abs(pnl)


                    self.loss_count +=1



                else:


                    self.win_count +=1







                if self.daily_loss >= MAX_DAILY_LOSS:



                    self.blocked=True



                    add_log(

                        "AUTO TRADE STOP LOSS LIMIT"

                    )







            update_status({


                "daily_loss":

                self.daily_loss,


                "wins":

                self.win_count,


                "losses":

                self.loss_count,


                "risk":

                "BLOCKED"

                if self.blocked

                else

                "OK"


            })






        except Exception as e:


            add_log(

                f"PNL ERROR {e}"

            )









    # =====================================================
    # LOSS STREAK
    # =====================================================

    def loss_streak(self):


        return self.loss_count







    # =====================================================
    # CAN TRADE
    # =====================================================

    def can_trade(self):


        return not self.blocked







    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "daily_loss":

            self.daily_loss,


            "orders":

            self.order_count,


            "wins":

            self.win_count,


            "losses":

            self.loss_count,


            "blocked":

            self.blocked

        }







    # =====================================================
    # RESET
    # =====================================================

    def reset(self):


        with self.lock:


            self.daily_loss=0

            self.order_count=0

            self.win_count=0

            self.loss_count=0

            self.blocked=False




        add_log(

            "RISK RESET"

        )









# =====================================================
# INSTANCE
# =====================================================

risk_manager=RiskManager()
