import time
import threading


from pybit.unified_trading import WebSocket


from config import (
    BYBIT_TESTNET,
    DEFAULT_SYMBOL
)



class WebSocketStream:


    def __init__(self):


        self.symbol = DEFAULT_SYMBOL


        self.ws = None


        print("==============================")
        print("[WEBSOCKET STREAM INIT]")
        print("TESTNET :", BYBIT_TESTNET)
        print("SYMBOL :", self.symbol)
        print("==============================")



    def start(self):


        self.ws = WebSocket(

            testnet=BYBIT_TESTNET,

            channel_type="linear"

        )


        self.ws.kline(

            interval=1,

            symbol=self.symbol,

            callback=self.callback

        )



        print(
            "[STREAM STARTED]"
        )



    def callback(
        self,
        message
    ):


        print(
            "[STREAM DATA]",
            message
        )




stream = WebSocketStream()
