# =====================================================
# app.py
# VWAP SUPERTREND AUTO BOT CORE
# =====================================================

import threading
import time



from api.bybit_api import (

    bybit_api

)



from services.private_ws import (

    private_ws

)



from portfolio.position_manager import (

    position_manager

)



from risk.risk_manager import (

    risk_manager

)



from order.order_manager import (

    order_manager

)



from web.server import (

    update_status,

    add_log

)









class TradingApp:



    def __init__(self):


        self.running = False


        self.market_thread = None


        self.stop_lock = threading.Lock()



        print(

            "[TRADING APP READY]"

        )









    # =====================================================
    # START
    # =====================================================

    def start(self):


        if self.running:


            return



        print()

        print("====================")

        print("[BOT START]")

        print("====================")




        self.running = True





        # -----------------------------
        # Balance Check
        # -----------------------------

        balance = bybit_api.get_balance()



        if balance:


            print(

                "[BALANCE OK]"

            )


        else:


            print(

                "[BALANCE CHECK FAILED]"

            )









        # -----------------------------
        # WS START
        # -----------------------------

        private_ws.start()







        # -----------------------------
        # Watchdog
        # -----------------------------

        try:


            from watchdog import watchdog



            watchdog.start()



            print(

                "[WATCHDOG START]"

            )


        except Exception as e:


            print(

                "[WATCHDOG ERROR]",

                e

            )









        # -----------------------------
        # MARKET LOOP
        # -----------------------------

        self.market_thread = threading.Thread(

            target=self.market_loop,

            daemon=True

        )


        self.market_thread.start()



        print(

            "[MARKET LOOP START]"

        )





        update_status({

            "bot":

                "RUNNING"

        })


        add_log(

            "BOT READY"

        )



        print()

        print(

            "[BOT READY]"

        )









    # =====================================================
    # MARKET LOOP
    # =====================================================

    def market_loop(self):


        while self.running:


            try:



                # =====================
                # 전략 위치
                # =====================

                #

                # strategy 모듈에서

                # signal 생성 후

                # order_manager 호출

                #



                time.sleep(

                    1

                )




            except Exception as e:


                add_log(

                    f"MARKET LOOP ERROR {e}"

                )



                time.sleep(

                    3

                )









    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        with self.stop_lock:



            if not self.running:


                return




            print()

            print("====================")

            print("[BOT STOP]")

            print("====================")





            self.running = False





            # -----------------------------
            # WS STOP
            # -----------------------------

            try:


                private_ws.stop()



            except Exception as e:


                print(

                    "[WS STOP ERROR]",

                    e

                )






            # -----------------------------
            # WATCHDOG STOP
            # -----------------------------

            try:


                from watchdog import watchdog



                watchdog.stop()



            except Exception as e:


                print(

                    "[WATCHDOG STOP ERROR]",

                    e

                )







            # -----------------------------
            # POSITION RESET
            # -----------------------------

            try:


                position_manager.close()



            except Exception as e:


                print(

                    "[POSITION CLOSE ERROR]",

                    e

                )






            update_status({

                "bot":

                    "STOPPED"

            })



            add_log(

                "BOT STOP COMPLETE"

            )



            print(

                "[BOT STOP COMPLETE]"

            )
