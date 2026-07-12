# =====================================================
# order/order_manager.py
# VWAP SUPERTREND BOT V3
# BYBIT V5 ORDER MANAGER
# =====================================================


import time


from api.bybit_api import bybit_api


from risk.risk_manager import risk_manager


from portfolio.position_manager import position_manager


from config import (
    TAKE_PROFIT_PERCENT,
    STOP_LOSS_PERCENT,
    MAX_POSITION_SIZE,
    TP1_PERCENT,
    TP2_PERCENT,
    TP3_PERCENT,
    TP1_SIZE,
    TP2_SIZE,
    TP3_SIZE
)


from web.server import (
    add_log,
    update_status
)







class OrderManager:



    def __init__(self):


        self.last_order_time = 0


        self.cooldown = 3



        print(

            "[ORDER MANAGER V3 READY]"

        )









    # =====================================================
    # COOLDOWN
    # =====================================================


    def can_order(self):


        if time.time() - self.last_order_time < self.cooldown:


            add_log(

                "ORDER COOLDOWN"

            )


            return False



        return True











    # =====================================================
    # BUY
    # =====================================================


    def buy(self, qty=None):


        return self.open_position(

            "Buy",

            qty

        )









    # =====================================================
    # SELL
    # =====================================================


    def sell(self, qty=None):


        return self.open_position(

            "Sell",

            qty

        )









    # =====================================================
    # OPEN POSITION
    # =====================================================


    def open_position(

        self,

        side,

        qty=None

    ):


        try:


            if not self.can_order():

                return False





            if qty is None:


                qty = MAX_POSITION_SIZE





            qty=float(qty)





            if not risk_manager.allow_order(qty):


                return False







            position = position_manager.get_position()



            current_side = position.get(

                "side",

                "NONE"

            )



            current_size=float(

                position.get(

                    "size",

                    0

                )

            )








            # SAME SIDE


            if current_size > 0 and current_side == side:


                add_log(

                    "SAME POSITION"

                )


                return False







            # REVERSE


            if current_size > 0 and current_side != side:


                add_log(

                    "CLOSE OPPOSITE"

                )


                if not self.close_position():

                    return False



                time.sleep(2)








            # LEVERAGE


            bybit_api.set_leverage()







            # ORDER


            result = bybit_api.place_order(

                side,

                qty,

                False

            )





            if not result:


                return False







            if result.get(

                "retCode",

                -1

            ) != 0:


                add_log(

                    str(result)

                )


                return False







            self.last_order_time=time.time()






            add_log(

                f"OPEN SUCCESS {side} {qty}"

            )



            update_status({

                "last_action":

                f"OPEN {side}"

            })






            time.sleep(1)



            position_manager.refresh()





            self.set_tp_sl()



            return True





        except Exception as e:


            add_log(

                f"OPEN ERROR {e}"

            )


            return False










    # =====================================================
    # TP / SL
    # =====================================================


    def set_tp_sl(self):


        try:


            pos=position_manager.get_position()



            side=pos.get(

                "side",

                ""

            )



            entry=float(

                pos.get(

                    "entry_price",

                    0

                )

            )




            if entry<=0:


                entry=bybit_api.get_price()





            if side=="Buy":


                tp1=entry*(1+TP1_PERCENT/100)

                tp2=entry*(1+TP2_PERCENT/100)

                tp3=entry*(1+TP3_PERCENT/100)



                sl=entry*(1-STOP_LOSS_PERCENT/100)





            elif side=="Sell":


                tp1=entry*(1-TP1_PERCENT/100)

                tp2=entry*(1-TP2_PERCENT/100)

                tp3=entry*(1-TP3_PERCENT/100)



                sl=entry*(1+STOP_LOSS_PERCENT/100)




            else:


                return False





            # BYBIT 기본 TP/SL


            result = bybit_api.set_trading_stop(

                round(tp1,2),

                round(sl,2)

            )





            add_log(

                f"TP1 {tp1} TP2 {tp2} TP3 {tp3} SL {sl}"

            )



            return result





        except Exception as e:


            add_log(

                f"TP SL ERROR {e}"

            )


            return False










    # =====================================================
    # MANUAL TP
    # =====================================================


    def set_take_profit(

        self,

        price

    ):


        return bybit_api.set_trading_stop(

            price,

            None

        )











    # =====================================================
    # MANUAL SL
    # =====================================================


    def set_stop_loss(

        self,

        price

    ):


        return bybit_api.set_trading_stop(

            None,

            price

        )









    # =====================================================
    # LEVERAGE
    # =====================================================


    def set_leverage(self):


        return bybit_api.set_leverage()










    # =====================================================
    # CLOSE
    # =====================================================


    def close(self):


        return self.close_position()






    def close_position(self):


        try:


            result=bybit_api.close_position()



            if result:


                position_manager.refresh()



                self.last_order_time=time.time()



                add_log(

                    "POSITION CLOSED"

                )



                update_status({

                    "last_action":

                    "POSITION CLOSED"

                })



                return True





            return False





        except Exception as e:


            add_log(

                f"CLOSE ERROR {e}"

            )


            return False











    # =====================================================
    # REVERSE
    # =====================================================


    def reverse_position(self):


        pos=position_manager.get_position()



        side=pos.get(

            "side",

            ""

        )



        size=float(

            pos.get(

                "size",

                0

            )

        )



        if size<=0:


            return False





        self.close_position()



        time.sleep(2)




        if side=="Buy":


            return self.sell(size)



        else:


            return self.buy(size)









    # =====================================================
    # EMERGENCY
    # =====================================================


    def emergency_close(self):


        add_log(

            "EMERGENCY CLOSE"

        )


        return self.close_position()











    # =====================================================
    # STATUS
    # =====================================================


    def status(self):


        return {


            "cooldown":

            self.cooldown,


            "last_order":

            self.last_order_time


        }









# =====================================================
# INSTANCE
# =====================================================


order_manager = OrderManager()
