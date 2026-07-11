# =======================================================
# app.py
# VWAP SuperTrend Trading Bot Core
# =======================================================

import time
import threading
import traceback

import config

from api.bybit_api import bybit_api
from services.private_ws import private_ws

from portfolio.position_manager import position_manager
from order.order_manager import order_manager
from risk.risk_manager import risk_manager

from web.server import (
    update_status,
    add_log
)


class TradingApp:


    def __init__(self):

        self.running = False

        self.market_thread = None

        self.stop_lock = threading.Lock()

        print("[거래 앱 준비 완료]")



    # =====================================================
    # START
    # =====================================================

    def start(self):

        if self.running:

            return


        print()
        print("====================")
        print("[봇 시작]")
        print("====================")


        self.running = True



        # -------------------------------------------------
        # API BALANCE CHECK
        # -------------------------------------------------

        try:

            balance = bybit_api.get_balance()


            if balance:

                print(
                    "[잔액 정상]"
                )

            else:

                print(
                    "[잔액 확인 실패 - 계속 진행]"
                )


        except Exception as e:

            print(
                "[잔액 API 보호 오류]",
                e
            )



        # -------------------------------------------------
        # PRIVATE WS START
        # -------------------------------------------------

        try:

            private_ws.start()

            print(
                "[PRIVATE WS START]"
            )


        except Exception as e:

            print(
                "[PRIVATE WS ERROR]",
                e
            )



        # -------------------------------------------------
        # POSITION SYNC
        # -------------------------------------------------

        try:

            position_manager.refresh()


        except Exception as e:

            print(
                "[POSITION REFRESH ERROR]",
                e
            )



        # -------------------------------------------------
        # WATCHDOG
        # -------------------------------------------------

        try:

            from services.watchdog import watchdog

            watchdog.start()

            print(
                "[WATCHDOG START]"
            )


        except Exception:

            pass



        # -------------------------------------------------
        # MARKET LOOP THREAD
        # -------------------------------------------------

        if (

            self.market_thread is None

            or not self.market_thread.is_alive()

        ):


            self.market_thread = threading.Thread(

                target=self.market_loop,

                daemon=True,

                name="MarketLoop"

            )


            self.market_thread.start()



        update_status({

            "bot":"RUNNING"

        })


        add_log(

            "BOT START"

        )


        print(

            "[BOT READY]"

        )




    # =====================================================
    # MARKET LOOP
    # =====================================================

    def market_loop(self):


        from market.market_data import market_data

        from strategy.vwap_supertrend import strategy



        print(

            "[MARKET LOOP START]"

        )



        while self.running:


            try:


                df = market_data.get_candles(

                    interval="5",

                    limit=200

                )


                if df is None:


                    time.sleep(5)

                    continue




                signal = strategy.generate_signal(

                    df

                )



                if signal:


                    print(

                        "[SIGNAL]",

                        signal

                    )


                    add_log(

                        f"SIGNAL {signal}"

                    )



                    position = (

                        position_manager
                        .get_position()

                    )



                    current = position.get(

                        "side",

                        "NONE"

                    )



                    if (

                        signal == "Buy"

                        and current == "Buy"

                    ):

                        add_log(

                            "SKIP EXIST BUY"

                        )

                        time.sleep(10)

                        continue



                    if (

                        signal == "Sell"

                        and current == "Sell"

                    ):


                        add_log(

                            "SKIP EXIST SELL"

                        )

                        time.sleep(10)

                        continue




                    qty = config.MAX_POSITION_SIZE



                    result = (

                        order_manager
                        .open_position(

                            signal,

                            qty

                        )

                    )



                    if result:


                        add_log(

                            f"ORDER SUCCESS {signal}"

                        )

                    else:


                        add_log(

                            "ORDER FAILED"

                        )




                time.sleep(10)



            except Exception as e:


                traceback.print_exc()


                add_log(

                    f"MARKET LOOP ERROR {e}"

                )


                time.sleep(5)




    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        with self.stop_lock:


            if not self.running:

                return



            print()

            print("====================")

            print("[봇 정지]")

            print("====================")



            self.running = False




            # -------------------------------------------------
            # CLOSE POSITION
            # -------------------------------------------------

            try:


                order_manager.close_position()


            except Exception as e:


                print(

                    "[CLOSE POSITION ERROR]",

                    e

                )




            # -------------------------------------------------
            # PRIVATE WS STOP
            # -------------------------------------------------

            try:


                private_ws.stop()


            except Exception as e:


                print(

                    "[PRIVATE WS STOP ERROR]",

                    e

                )




            # -------------------------------------------------
            # WATCHDOG STOP
            # -------------------------------------------------

            try:


                from services.watchdog import watchdog


                watchdog.stop()


            except Exception:

                pass




            # -------------------------------------------------
            # THREAD JOIN
            # -------------------------------------------------

            if (

                self.market_thread

                and self.market_thread.is_alive()

            ):


                self.market_thread.join(

                    timeout=5

                )



            self.market_thread = None



            update_status({

                "bot":"STOPPED"

            })



            add_log(

                "BOT STOP"

            )


            print(

                "[BOT STOP COMPLETE]"

            )



# =====================================================
# INSTANCE
# =====================================================

trading_app = TradingApp()
