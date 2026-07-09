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


        print("==============================")
        print("[WEBSOCKET STREAM INIT]")
        print("TESTNET :", TESTNET)
        print("SYMBOL  :", self.symbol)
        print("==============================")


    # ==================================
    # START
    # ==================================

    def start(self):

        self.ws = WebSocket(

            testnet=TESTNET,

            channel_type="linear"

        )


        self.ws.kline(

            interval=5,

            symbol=self.symbol,

            callback=self.callback

        )


        print(
            "[STREAM STARTED]"
        )


        while True:

            time.sleep(1)



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


            # 완성 캔들 확인

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



            # 중복 방지

            if candle["timestamp"] == self.last_timestamp:

                return


            self.last_timestamp = candle["timestamp"]



            print(
                "[CANDLE]",
                candle
            )


            # Indicator 업데이트

            indicator_engine.update(
                candle
            )


            # Strategy 실행

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
    # THREAD
    # ==================================

    def run_thread(self):

        thread = threading.Thread(

            target=self.start,

            daemon=True

        )


        thread.start()



stream = WebSocketStream()
