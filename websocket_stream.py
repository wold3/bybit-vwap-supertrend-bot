import time
import threading


from pybit.unified_trading import WebSocket


from config import (
    TESTNET,
    DEFAULT_SYMBOL,
)


from indicators.indicator_engine import indicator_engine
from strategy.strategy_engine import strategy_engine





class WebSocketStream:


    def __init__(self):

        self.symbol = DEFAULT_SYMBOL

        self.ws = None

        self.last_timestamp = None

        self.running = False


        print("==============================")
        print("[WEBSOCKET STREAM INIT]")
        print("TESTNET :", TESTNET)
        print("SYMBOL  :", self.symbol)
        print("==============================")





    # ==================================
    # START
    # ==================================

    def start(self):


        if self.running:

            return


        self.running = True



        try:


            self.ws = WebSocket(

                testnet=TESTNET,

                channel_type="linear"

            )



            self.ws.kline_stream(

                interval=5,

                symbol=self.symbol,

                callback=self.callback

            )



            print(
                "[STREAM STARTED]"
            )



            while self.running:


                time.sleep(1)



        except Exception as e:


            print(
                "[WEBSOCKET START ERROR]",
                e
            )






    # ==================================
    # CALLBACK
    # ==================================

    def callback(
        self,
        message
    ):


        try:


            if "data" not in message:

                return



            data = message["data"]



            if not data:

                return



            candle_data = data[0]



            if not candle_data.get(
                "confirm",
                False
            ):

                return




            candle = {


                "symbol":
                    self.symbol,



                "timestamp":
                    int(
                        candle_data["start"]
                    ),



                "open":
                    float(
                        candle_data["open"]
                    ),



                "high":
                    float(
                        candle_data["high"]
                    ),



                "low":
                    float(
                        candle_data["low"]
                    ),



                "close":
                    float(
                        candle_data["close"]
                    ),



                "volume":
                    float(
                        candle_data["volume"]
                    ),



                "confirm":
                    True

            }




            # 중복 캔들 방지

            if candle["timestamp"] == self.last_timestamp:

                return



            self.last_timestamp = candle["timestamp"]



            print(
                "[CANDLE]",
                candle
            )





            # Indicator

            indicators = indicator_engine.update(

                candle

            )



            if not indicators:

                return





            # Strategy

            signal = strategy_engine.on_candle(

                candle

            )



            if signal:


                print(
                    "[SIGNAL]",
                    signal
                )





        except Exception as e:


            print(
                "[WS CALLBACK ERROR]",
                e
            )







    # ==================================
    # STOP
    # ==================================

    def stop(self):


        self.running = False



        try:

            if self.ws:

                self.ws.exit()

        except Exception:


            pass



        print(
            "[STREAM STOPPED]"
        )






    # ==================================
    # THREAD
    # ==================================

    def run_thread(self):


        thread = threading.Thread(

            target=self.start,

            daemon=True

        )


        thread.start()






stream = WebSocketStream()
