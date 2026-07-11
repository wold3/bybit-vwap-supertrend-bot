# =====================================================
# app.py
# VWAP SUPERTREND BOT APPLICATION
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

                "RUNNING"

        })



        add_log(

            "BOT START"

        )



        self.market_thread = threading.Thread(

            target=self.market_loop,

            daemon=True,

            name="MarketLoop"

        )


        self.market_thread.start()



        add_log(

            "BOT START COMPLETE"

        )



        return True









    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        with self.lock:


            if not self.running:


                return False



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



                # -------------------------
                # POSITION SYNC
                # -------------------------

                position_manager.refresh()





                # -------------------------
                # MARKET DATA
                # -------------------------

                df = market_data.get_candles(


                    interval="5",


                    limit=200


                )



                if df is None:


                    time.sleep(5)

                    continue







                # -------------------------
                # STRATEGY
                # -------------------------

                signal = strategy.generate_signal(

                    df

                )




                if signal:



                    price = market_data.price()



                    add_log(

                        f"SIGNAL {signal}"

                    )




                    update_status({

                        "last_action":

                            f"SIGNAL {signal}",


                        "mark_price":

                            price

                    })





                    # -------------------------
                    # ORDER EXECUTION
                    # -------------------------

                    order_manager.open_position(

                        signal

                    )







                time.sleep(5)





            except Exception as e:



                add_log(

                    f"MARKET LOOP ERROR {e}"

                )


                time.sleep(5)







        add_log(

            "MARKET LOOP STOP"

        )









    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "running":

                self.running

        }







# =====================================================
# INSTANCE
# =====================================================

trading_app = TradingApp()
