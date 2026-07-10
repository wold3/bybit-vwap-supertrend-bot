import threading
import time


from websocket.public_ws import (
    ws_client,
)


from websocket.private_ws import (
    private_ws_client,
)


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


from guard.bot_guard import (
    bot_guard,
)


from watchdog.watchdog import (
    watchdog,
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







        # Public WS callback 연결

        ws_client.set_callback(

            self.on_candle

        )









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





        # Risk 초기화

        risk_manager.initialize()






        # Watchdog

        watchdog.start()







        # Private WS

        threading.Thread(

            target=private_ws_client.start,

            daemon=True

        ).start()







        # Public WS

        ws_client.start()







        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )


        self.thread.start()





        print(
            "[BOT RUNNING]"
        )









    # =====================================================
    # CANDLE CALLBACK
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
                    "[SIGNAL BUY]"
                )



                order_manager.buy()






            elif signal == "SELL":



                print(
                    "[SIGNAL SELL]"
                )



                order_manager.sell()







        except Exception as e:


            print(

                "[CANDLE PROCESS ERROR]",

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

                    "[APP LOOP ERROR]",

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



        bot_guard.stop()



        ws_client.stop()



        private_ws_client.stop()



        watchdog.stop()



        print(
            "[BOT STOPPED]"
        )











app = TradingApp()
