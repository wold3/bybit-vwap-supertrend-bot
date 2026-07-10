# =====================================================
# services/watchdog.py
# =====================================================

import time
import threading


from api.bybit_api import (
    bybit_api
)


from order.order_manager import (
    order_manager
)


from config import (
    WATCHDOG_INTERVAL,
    MAX_API_ERROR,
    STOP_LOSS_PERCENT,
    TAKE_PROFIT_PERCENT
)



class Watchdog:


    def __init__(self):

        self.running = False

        self.thread = None

        self.last_heartbeat = time.time()

        self.api_error_count = 0

        self.system_ok = True


        print(
            "[WATCHDOG READY]"
        )



    # =====================================================
    # START
    # =====================================================

    def start(self):

        if self.running:

            return


        self.running = True


        self.thread = threading.Thread(

            target=self.monitor

        )


        self.thread.daemon = True


        self.thread.start()


        print(
            "[WATCHDOG START]"
        )



    # =====================================================
    # LOOP
    # =====================================================

    def monitor(self):


        while self.running:


            try:


                self.check_api()


                self.check_position()


                self.check_health()



            except Exception as e:


                print(
                    "[WATCHDOG ERROR]",
                    e
                )



            time.sleep(

                WATCHDOG_INTERVAL

            )



    # =====================================================
    # API CHECK
    # =====================================================

    def check_api(self):


        result = (

            bybit_api
            .ping()

        )



        if result:


            self.api_error_count = 0

            self.system_ok = True



        else:


            self.api_error_count += 1



            print(

                "[API ERROR COUNT]",

                self.api_error_count

            )



            if self.api_error_count >= MAX_API_ERROR:


                self.emergency_stop()



    # =====================================================
    # POSITION MONITOR
    # =====================================================

    def check_position(self):


        try:


            position = (

                bybit_api
                .get_position()

            )



            if position is None:

                return



            rows = (

                position

                .get(

                    "result",

                    {}

                )

                .get(

                    "list",

                    []

                )

            )



            for p in rows:



                size = float(

                    p.get(

                        "size",

                        0

                    )

                )



                if size <= 0:

                    continue



                side = p.get(

                    "side"

                )



                entry = float(

                    p.get(

                        "avgPrice",

                        0

                    )

                )



                price = (

                    bybit_api

                    .get_last_price()

                )



                if price is None:

                    return



                if entry <= 0:

                    return



                if side == "Buy":


                    pnl = (

                        (price-entry)

                        /

                        entry

                    ) * 100



                else:


                    pnl = (

                        (entry-price)

                        /

                        entry

                    ) * 100





                print(

                    "[POSITION MONITOR]",

                    side,

                    round(

                        pnl,

                        3

                    ),

                    "%"

                )





                # -----------------------------
                # STOP LOSS
                # -----------------------------

                if pnl <= -STOP_LOSS_PERCENT:


                    print(

                        "[STOP LOSS]"

                    )


                    order_manager.close_position()


                    return





                # -----------------------------
                # TAKE PROFIT
                # -----------------------------

                if pnl >= TAKE_PROFIT_PERCENT:


                    print(

                        "[TAKE PROFIT]"

                    )


                    order_manager.close_position()


                    return




        except Exception as e:


            print(

                "[POSITION CHECK ERROR]",

                e

            )



    # =====================================================
    # HEALTH CHECK
    # =====================================================

    def check_health(self):


        now = time.time()



        if (

            now - self.last_heartbeat

            >

            WATCHDOG_INTERVAL * 5

        ):


            print(

                "[WATCHDOG WARNING] NO HEARTBEAT"

            )



    # =====================================================
    # HEARTBEAT
    # =====================================================

    def heartbeat(self):


        self.last_heartbeat = time.time()



    # =====================================================
    # EMERGENCY STOP
    # =====================================================

    def emergency_stop(self):


        print(
            "==================="
        )

        print(
            "[WATCHDOG EMERGENCY STOP]"
        )

        print(
            "API FAILURE"
        )

        print(
            "==================="
        )


        self.system_ok = False



    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "running":

                self.running,


            "system_ok":

                self.system_ok,


            "api_errors":

                self.api_error_count,


            "heartbeat":

                self.last_heartbeat


        }



    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        self.running = False


        print(

            "[WATCHDOG STOP]"

        )





# =====================================================
# SINGLETON
# =====================================================

watchdog = Watchdog()
