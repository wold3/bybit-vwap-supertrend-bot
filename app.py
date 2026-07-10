import threading
import time


from websocket_stream import stream


from indicators.indicator_engine import (
    indicator_engine,
)


from strategy.strategy_engine import (
    strategy_engine,
)


from execution.order_manager import (
    order_manager,
)


from risk.risk_manager import (
    risk_manager,
)


from watchdog.watchdog import (
    watchdog,
)


from guard.bot_guard import (
    bot_guard,
)


from portfolio.bybit_wallet import (
    wallet,
)





class TradingApp:


    def __init__(self):

        print("==============================")
        print("[APP INIT]")
        print("==============================")


        self.running = False

        self.thread = None



    # =====================================================
    # START
    # =====================================================

    def start(self):


        if self.running:

            return



        self.running = True


        print("==============================")
        print("VWAP SUPERTREND BOT START")
        print("==============================")



        # Risk

        try:

            risk_manager.initialize()

        except Exception as e:

            print(
                "[RISK INIT ERROR]",
                e
            )



        # Watchdog

        try:

            watchdog.start()

        except Exception as e:

            print(
                "[WATCHDOG ERROR]",
                e
            )




        # Websocket 시작

        threading.Thread(

            target=stream.start,

            daemon=True

        ).start()



        # Main Loop

        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )


        self.thread.start()



        print(
            "[BOT RUNNING]"
        )





    # =====================================================
    # CANDLE PROCESS
    # =====================================================

    def on_candle(
        self,
        candle
    ):


        if not bot_guard.is_running():

            return



        try:


            indicators = indicator_engine.update(

                candle

            )



            if not indicators:

                return



            signal = strategy_engine.analyze(

                candle,

                indicators

            )



            if signal == "BUY":


                print(
                    "[BUY SIGNAL]"
                )


                order_manager.buy()



            elif signal == "SELL":


                print(
                    "[SELL SIGNAL]"
                )


                order_manager.sell()



        except Exception as e:


            print(
                "[CANDLE ERROR]",
                e
            )







    # =====================================================
    # LOOP
    # =====================================================

    def loop(self):


        print(
            "[APP LOOP START]"
        )


        while self.running:


            try:


                watchdog.heartbeat()



                risk_manager.check_daily_loss()



                time.sleep(5)



            except Exception as e:


                print(
                    "[LOOP ERROR]",
                    e
                )


                time.sleep(5)






    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        print(
            "[BOT STOPPING]"
        )


        self.running = False



        try:

            bot_guard.stop()

        except:

            pass



        try:

            watchdog.stop()

        except:

            pass



        print(
            "[BOT STOPPED]"
        )






app = TradingApp()
