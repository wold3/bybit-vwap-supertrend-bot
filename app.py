# =====================================================
# app.py
# VWAP SUPERTREND BOT V2
# AUTO TRADING APPLICATION
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



        print(

            "[BOT V2 READY]"

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





            self.running=True






        set_bot(

            self

        )





        update_status({

            "bot":

            "RUNNING"

        })





        add_log(

            "BOT START"

        )






        self.market_thread = threading.Thread(


            target=self.market_loop,


            daemon=True


        )



        self.market_thread.start()





        add_log(

            "AUTO TRADE ENABLED"

        )



        return True










    # =====================================================
    # STOP
    # =====================================================


    def stop(self):


        with self.lock:


            self.running=False





        add_log(

            "BOT STOP"

        )



        update_status({

            "bot":

            "STOPPED"

        })



        return True











    # =====================================================
    # MARKET LOOP
    # =====================================================


    def market_loop(self):


        add_log(

            "MARKET LOOP START"

        )





        while self.running:



            try:



                # ---------------------------------
                # POSITION UPDATE
                # ---------------------------------


                position_manager.refresh()






                # ---------------------------------
                # TP / TRAILING CHECK
                # ---------------------------------


                order_manager.check_take_profit()



                order_manager.check_trailing_stop()






                pos = position_manager.get_position()





                update_status({


                    "current_position":

                    pos



                })








                # ---------------------------------
                # GET MARKET DATA
                # ---------------------------------


                df = market_data.get_candles(


                    interval="5",


                    limit=200


                )





                if df is None:


                    time.sleep(5)


                    continue







                # ---------------------------------
                # STRATEGY SIGNAL
                # ---------------------------------


                signal = strategy.generate_signal(

                    df

                )






                if signal:



                    price = market_data.price()



                    add_log(

                        f"SIGNAL {signal}"

                    )






                    update_status({


                        "signal":

                        signal,


                        "price":

                        price



                    })








                    # ---------------------------------
                    # AUTO ORDER
                    # ---------------------------------


                    order_manager.open_position(


                        signal


                    )








                time.sleep(5)






            except Exception as e:



                add_log(

                    f"LOOP ERROR {e}"

                )



                time.sleep(5)






        add_log(

            "MARKET LOOP STOP"

        )

    # =====================================================
    # MANUAL BUY
    # =====================================================


    def buy(self, qty=None):


        try:


            add_log(

                "MANUAL BUY"

            )


            return order_manager.buy(

                qty

            )



        except Exception as e:


            add_log(

                f"BUY ERROR {e}"

            )


            return False










    # =====================================================
    # MANUAL SELL
    # =====================================================


    def sell(self, qty=None):


        try:


            add_log(

                "MANUAL SELL"

            )


            return order_manager.sell(

                qty

            )



        except Exception as e:


            add_log(

                f"SELL ERROR {e}"

            )


            return False










    # =====================================================
    # CLOSE
    # =====================================================


    def close(self):


        try:


            add_log(

                "MANUAL CLOSE"

            )


            return order_manager.close_position()



        except Exception as e:


            add_log(

                f"CLOSE ERROR {e}"

            )


            return False










    # =====================================================
    # REVERSE
    # =====================================================


    def reverse(self):


        try:


            return order_manager.reverse_position()



        except Exception as e:


            add_log(

                f"REVERSE ERROR {e}"

            )


            return False










    # =====================================================
    # LEVERAGE
    # =====================================================


    def set_leverage(self):


        try:


            return order_manager.set_leverage()



        except Exception as e:


            add_log(

                f"LEV ERROR {e}"

            )


            return False










    # =====================================================
    # STATUS
    # =====================================================


    def status(self):


        return {


            "running":

            self.running,



            "position":

            position_manager.get_position(),



            "order":

            order_manager.status()



        }









# =====================================================
# INSTANCE
# =====================================================


trading_app = TradingApp()
