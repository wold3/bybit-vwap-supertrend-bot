# =====================================================
# order/order_manager.py
# VWAP SUPERTREND BOT V2
# BYBIT V5 ORDER MANAGER
# AUTO TRADE + SCALE IN + TP/SL
# =====================================================


import time
import threading



from api.bybit_api import bybit_api


from portfolio.position_manager import position_manager


from risk.risk_manager import risk_manager



from config import (

    MAX_POSITION_SIZE,

    LEVERAGE,

    ENTRY1_PERCENT,

    ENTRY2_PERCENT,

    TP1_PERCENT,

    TP2_PERCENT,

    TP3_PERCENT,

    TP1_CLOSE_SIZE,

    TP2_CLOSE_SIZE,

    TP3_CLOSE_SIZE,

    STOP_LOSS_PERCENT,

    TRAILING_STOP,

    TRAILING_DISTANCE,

    ORDER_COOLDOWN

)



from web.server import (

    add_log,

    update_status

)







class OrderManager:



    def __init__(self):


        self.last_order_time = 0


        self.cooldown = ORDER_COOLDOWN


        self.lock = threading.Lock()



        self.tp_stage = 0


        self.highest_profit = 0



        print(

            "[ORDER MANAGER V2 READY]"

        )









    # =====================================================
    # COOLDOWN
    # =====================================================


    def can_order(self):


        return (

            time.time()

            -

            self.last_order_time

            >

            self.cooldown

        )









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


            with self.lock:



                if not self.can_order():


                    add_log(

                        "ORDER COOLDOWN"

                    )

                    return False





                if qty is None:


                    qty = MAX_POSITION_SIZE






                qty=float(qty)





                if not risk_manager.allow_order(qty):


                    return False





                position = position_manager.get_position()



                current_size = float(

                    position.get(

                        "size",

                        0

                    )

                )



                current_side = position.get(

                    "side",

                    "NONE"

                )






                # 같은 방향 보유


                if current_size > 0 and current_side == side:


                    add_log(

                        "POSITION EXISTS"

                    )


                    return False






                # 반대 방향이면 종료 후 진입


                if current_size > 0 and current_side != side:


                    self.close_position()


                    time.sleep(2)







                # 레버리지


                bybit_api.set_leverage()






                result = bybit_api.place_order(

                    side,

                    qty,

                    False

                )





                if not result:


                    add_log(

                        "ORDER FAILED"

                    )

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


                self.tp_stage=0


                self.highest_profit=0





                add_log(

                    f"OPEN SUCCESS {side} {qty}"

                )




                update_status({


                    "position":side,


                    "last_action":

                    f"OPEN {side}",


                    "leverage":

                    LEVERAGE


                })





                time.sleep(1)



                position_manager.refresh()



                self.set_tp_sl()





                return result





        except Exception as e:


            add_log(

                f"OPEN ERROR {e}"

            )


            return False

    # =====================================================
    # TP / SL SET
    # =====================================================


    def set_tp_sl(self):


        try:


            pos = position_manager.get_position()



            side = pos.get(

                "side",

                ""

            )



            entry = float(

                pos.get(

                    "entry_price",

                    0

                )

            )




            if entry <= 0:


                entry = bybit_api.get_price()





            if not entry:


                return False






            if side == "Buy":


                sl = entry * (

                    1 -

                    STOP_LOSS_PERCENT / 100

                )



            elif side == "Sell":


                sl = entry * (

                    1 +

                    STOP_LOSS_PERCENT / 100

                )



            else:


                return False





            result = bybit_api.set_trading_stop(


                None,


                round(sl,2)


            )





            add_log(

                f"STOP LOSS {sl}"

            )



            return result





        except Exception as e:


            add_log(

                f"SET SL ERROR {e}"

            )


            return False









    # =====================================================
    # CURRENT PROFIT %
    # =====================================================


    def profit_percent(self):


        try:


            pos = position_manager.get_position()



            side = pos.get(

                "side",

                ""

            )



            entry = float(

                pos.get(

                    "entry_price",

                    0

                )

            )



            price = float(

                bybit_api.get_price()

            )





            if entry <= 0:


                return 0






            if side == "Buy":


                return (

                    price-entry

                ) / entry * 100





            elif side == "Sell":


                return (

                    entry-price

                ) / entry * 100





            return 0





        except:


            return 0










    # =====================================================
    # AUTO TP CHECK
    # =====================================================


    def check_take_profit(self):


        try:


            pnl = self.profit_percent()



            update_status({


                "profit_percent":

                round(pnl,2)


            })





            if pnl <= 0:


                return False







            # TP1


            if (

                self.tp_stage == 0

                and

                pnl >= TP1_PERCENT

            ):


                self.partial_close(

                    TP1_CLOSE_SIZE

                )


                self.tp_stage = 1



                add_log(

                    "TP1 COMPLETE"

                )







            # TP2


            elif (

                self.tp_stage == 1

                and

                pnl >= TP2_PERCENT

            ):


                self.partial_close(

                    TP2_CLOSE_SIZE

                )


                self.tp_stage = 2



                add_log(

                    "TP2 COMPLETE"

                )









            # TP3 FULL CLOSE


            elif (

                self.tp_stage == 2

                and

                pnl >= TP3_PERCENT

            ):


                self.close_position()


                self.tp_stage = 3



                add_log(

                    "TP3 COMPLETE CLOSE"

                )





            return True





        except Exception as e:


            add_log(

                f"TP CHECK ERROR {e}"

            )


            return False











    # =====================================================
    # PARTIAL CLOSE
    # =====================================================


    def partial_close(

        self,

        percent

    ):


        try:


            pos = position_manager.get_position()



            size = float(

                pos.get(

                    "size",

                    0

                )

            )



            if size <= 0:


                return False





            qty = size * (

                percent / 100

            )





            side = pos.get(

                "side",

                ""

            )





            if side == "Buy":


                close_side="Sell"



            elif side=="Sell":


                close_side="Buy"



            else:


                return False





            result = bybit_api.place_order(


                close_side,


                round(qty,6),


                True


            )





            if result:


                add_log(

                    f"PARTIAL CLOSE {percent}%"

                )


                time.sleep(1)


                position_manager.refresh()



                return True





            return False





        except Exception as e:


            add_log(

                f"PARTIAL CLOSE ERROR {e}"

            )


            return False

    # =====================================================
    # TRAILING STOP
    # =====================================================


    def check_trailing_stop(self):


        try:


            if not TRAILING_STOP:


                return False




            pnl = self.profit_percent()



            if pnl <= 0:


                return False






            if pnl > self.highest_profit:


                self.highest_profit = pnl






            if (

                self.highest_profit

                -

                pnl

                >=

                TRAILING_DISTANCE

            ):


                add_log(

                    "TRAILING STOP"

                )


                self.close_position()



                return True





            return False





        except Exception as e:


            add_log(

                f"TRAILING ERROR {e}"

            )


            return False










    # =====================================================
    # MANUAL TAKE PROFIT
    # =====================================================


    def set_take_profit(

        self,

        price

    ):


        try:


            return bybit_api.set_trading_stop(


                price,


                None


            )



        except Exception as e:


            add_log(

                f"MANUAL TP ERROR {e}"

            )


            return False











    # =====================================================
    # MANUAL STOP LOSS
    # =====================================================


    def set_stop_loss(

        self,

        price

    ):


        try:


            return bybit_api.set_trading_stop(


                None,


                price


            )



        except Exception as e:


            add_log(

                f"MANUAL SL ERROR {e}"

            )


            return False











    # =====================================================
    # LEVERAGE
    # =====================================================


    def set_leverage(self):


        try:


            result = bybit_api.set_leverage()



            add_log(

                f"LEVERAGE {LEVERAGE}X"

            )



            return result





        except Exception as e:


            add_log(

                f"LEVERAGE ERROR {e}"

            )


            return False











    # =====================================================
    # CLOSE POSITION
    # =====================================================


    def close_position(self):


        try:



            result = bybit_api.close_position()



            if result:



                time.sleep(1)


                position_manager.refresh()



                self.tp_stage = 0


                self.highest_profit = 0



                add_log(

                    "POSITION CLOSED"

                )



                update_status({


                    "position":

                    "NONE",


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
    # REVERSE POSITION
    # =====================================================


    def reverse_position(self):


        try:


            pos = position_manager.get_position()



            side = pos.get(

                "side",

                ""

            )



            size = float(

                pos.get(

                    "size",

                    0

                )

            )





            if size <= 0:


                return False






            if not self.close_position():


                return False





            time.sleep(2)





            if side == "Buy":


                return self.sell(size)



            elif side == "Sell":


                return self.buy(size)



            return False





        except Exception as e:


            add_log(

                f"REVERSE ERROR {e}"

            )


            return False










    # =====================================================
    # EMERGENCY CLOSE
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

                self.last_order_time,


            "tp_stage":

                self.tp_stage,


            "highest_profit":

                self.highest_profit


        }







# =====================================================
# INSTANCE
# =====================================================


order_manager = OrderManager()
