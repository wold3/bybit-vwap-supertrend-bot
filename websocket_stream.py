import time
import threading

from pybit.unified_trading import WebSocket

from config import (
    TESTNET,
    DEFAULT_SYMBOL,
)


class WebSocketStream:


    def __init__(self):

        self.symbol = DEFAULT_SYMBOL

        self.ws = None

        self.callback_func = None

        self.last_timestamp = None


        print("==============================")
        print("[WEBSOCKET STREAM INIT]")
        print("TESTNET :", TESTNET)
        print("SYMBOL  :", self.symbol)
        print("==============================")



    def set_callback(self, callback):

        self.callback_func = callback



    # ==================================
    # START
    # ==================================

    def start(self):

        print("[PUBLIC WS START]")


        self.ws = WebSocket(

            testnet=TESTNET,

            channel_type="linear"

        )


        self.ws.kline_stream(

            interval=5,

            symbol=self.symbol,

            callback=self.callback

        )


        print("[STREAM STARTED]")


        while True:

            time.sleep(1)



    # ==================================
    # CALLBACK
    # ==================================

    def callback(self, message):

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



            if candle["timestamp"] == self.last_timestamp:

                return


            self.last_timestamp = candle["timestamp"]



            print(
                "[CANDLE]",
                candle
            )



            if self.callback_func:

                self.callback_func(
                    candle
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

        t = threading.Thread(

            target=self.start,

            daemon=True

        )

        t.start()



stream = WebSocketStream()
