import time
import threading

from pybit.unified_trading import WebSocket

from config import (
    BYBIT_TESTNET,
    BYBIT_DEMO,
    CATEGORY,
    DEFAULT_SYMBOL,
)


class PublicWS:


    def __init__(self):

        self.ws = None
        self.running = False

        self.ticker = None
        self.kline = []

        print("==============================")
        print("[PUBLIC WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")


    # ==========================
    # CALLBACK
    # ==========================

    def handle_ticker(self, message):

        try:

            self.ticker = message


        except Exception as e:

            print(
                "[TICKER ERROR]",
                e
            )



    def handle_kline(self, message):

        try:

            data = message.get(
                "data",
                []
            )


            for candle in data:

                self.kline.append(candle)


            if len(self.kline) > 300:

                self.kline = self.kline[-300:]


        except Exception as e:

            print(
                "[KLINE ERROR]",
                e
            )



    # ==========================
    # START
    # ==========================

    def start(self):

        try:

            self.running = True


            self.ws = WebSocket(

                testnet=BYBIT_TESTNET,

                demo=BYBIT_DEMO,

                channel_type="linear"

            )


            self.ws.ticker_stream(

                symbol=DEFAULT_SYMBOL,

                callback=self.handle_ticker

            )


            self.ws.kline_stream(

                interval=1,

                symbol=DEFAULT_SYMBOL,

                callback=self.handle_kline

            )


            print(
                "[PUBLIC WS STARTED]"
            )


            while self.running:

                time.sleep(1)



        except Exception as e:

            print(
                "[PUBLIC WS START ERROR]",
                e
            )



    # ==========================
    # THREAD
    # ==========================

    def run_thread(self):

        thread = threading.Thread(

            target=self.start,

            daemon=True

        )

        thread.start()



    # ==========================
    # STOP
    # ==========================

    def stop(self):

        self.running = False

        print(
            "[PUBLIC WS STOPPED]"
        )



    # ==========================
    # GET
    # ==========================

    def get_price(self):

        try:

            if self.ticker:

                return float(
                    self.ticker["data"]["lastPrice"]
                )


        except:

            pass


        return None



public_ws = PublicWS()
