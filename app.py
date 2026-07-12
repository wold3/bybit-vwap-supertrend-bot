# =====================================================
# app.py
# VWAP SUPERTREND BOT APPLICATION
# AUTO TRADING ENGINE
# =====================================================


import threading
import time



from web.server import (

    add_log,

    update_status,

    set_bot

)



from market.market_data import market_data


from strategy.vwap_supertrend import strategy


from order.order_manager import order_manager


from portfolio.position_manager import position_manager







class TradingApp:



    def __init__(self):


        self.running = False


        self.market_thread = None


        self.lock = threading.Lock()



        # 중복 신호 방지

        self.last_signal = None

        self.last_signal_time = 0



        print(

            "[BOT READY]"

        )









    # =====================================================
    # START
    # =====================================================

    def start(self):


        with self.lock:


            if self.running:


                add_log(

                    "BOT ALREADY RUNNING"

                )


                return False



            self.running = True




        set_bot(

            self

        )





        update_status({

            "bot":

            "RUNNING",


            "auto_trade":

            "ON"

        })





        add_log(

            "AUTO TRADING START"

        )





        self.market_thread = threading.Thread(


            target=self.market_loop,


            daemon=True,


            name="AUTO-TRADING"

        )



        self.market_thread.start()




        add_log(

            "MARKET LOOP START"

        )



        return True










    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        with self.lock:


            if not self.running:


                return False



            self.running = False





        update_status({

            "bot":

            "STOPPED",


            "auto_trade":

            "OFF"

        })





        add_log(

            "AUTO TRADING STOP"

        )



        return True










    # =====================================================
    # MARKET LOOP
    # =====================================================

    def market_loop(self):


        add_log(

            "AUTO ENGINE RUN"

        )



        while self.running:


            try:




                # -----------------------------
                # POSITION UPDATE
                # -----------------------------

                position_manager.refresh()





                # -----------------------------
                # MARKET DATA
                # -----------------------------

                df = market_data.get_candles(


                    interval="5",


                    limit=200

                )





                if df is None:


                    add_log(

                        "NO MARKET DATA"

                    )


                    time.sleep(5)


                    continue







                # -----------------------------
                # STRATEGY SIGNAL
                # -----------------------------

                signal = strategy.generate_signal(

                    df

                )







                # -----------------------------
                # PRICE UPDATE
                # -----------------------------

                try:


                    price = market_data.price()



                except:


                    price = 0






                update_status({

                    "price":

                    price,


                    "mark_price":

                    price

                })








                # -----------------------------
                # ORDER CHECK
                # -----------------------------

                if signal:



                    now = time.time()



                    # 같은 신호 5분 차단

                    if (


                        signal == self.last_signal

                        and

                        now - self.last_signal_time < 300


                    ):


                        time.sleep(5)


                        continue







                    self.last_signal = signal


                    self.last_signal_time = now





                    add_log(

                        f"SIGNAL {signal}"

                    )





                    update_status({

                        "last_action":

                        f"SIGNAL {signal}"

                    })







                    result = order_manager.open_position(


                        signal

                    )






                    if result:


                        add_log(

                            f"AUTO ORDER {signal}"

                        )



                    else:


                        add_log(

                            "ORDER SKIPPED"

                        )










                # -----------------------------
                # LOOP DELAY
                # -----------------------------


                time.sleep(5)









            except Exception as e:



                add_log(

                    f"AUTO LOOP ERROR {e}"

                )



                time.sleep(5)










        add_log(

            "AUTO ENGINE STOP"

        )









    # =====================================================
    # MANUAL BUY
    # =====================================================

    def buy(self,qty=None):


        return order_manager.open_position(

            "Buy",

            qty

        )









    # =====================================================
    # MANUAL SELL
    # =====================================================

    def sell(self,qty=None):


        return order_manager.open_position(

            "Sell",

            qty

        )









    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):


        return order_manager.close_position()










    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "running":

            self.running,


            "last_signal":

            self.last_signal


        }









# =====================================================
# INSTANCE
# =====================================================


trading_app = TradingApp()
