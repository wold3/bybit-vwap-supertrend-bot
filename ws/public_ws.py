import threading
import time

from pybit.unified_trading import WebSocket

from config import (
    BYBIT_TESTNET,
    CATEGORY,
    DEFAULT_SYMBOL,
)


# ==========================================
# PUBLIC WEBSOCKET V5
# ==========================================

class PublicWS:


    def __init__(self):

        self.ws = None

        self.running = False

        self.price = None

        self.kline = []

        print("==============================")
        print("[PUBLIC WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")



    # ======================================
    # TICKER CALLBACK
    # ======================================

    def ticker_callback(self, message):

        try:

            data = message.get("data")


            if not data:
                return


            if isinstance(data, list):

                data = data[0]


            last_price = data.get("lastPrice")


            if last_price:

                self.price = float(last_price)



        except Exception as e:

            print(
                "[PUBLIC WS TICKER ERROR]",
                e
            )



    # ======================================
    # KLINE CALLBACK
    # ======================================

    def kline_callback(self, message):

        try:

            data = message.get("data")


            if not data:
                return


            for candle in data:


                close = candle.get("close")


                if close:


                    self.kline.append(
                        float(close)
                    )


                    # 최근 200개 유지

                    if len(self.kline) > 200:

                        self.kline.pop(0)



        except Exception as e:

            print(
                "[PUBLIC WS KLINE ERROR]",
                e
            )



    # ======================================
    # START
    # ======================================

    def start(self):


        if self.running:

            return


        try:


            self.running = True



            self.ws = WebSocket(

                testnet=BYBIT_TESTNET,

                channel_type="linear"

            )



            # ticker

            self.ws.ticker_stream(

                symbol=DEFAULT_SYMBOL,

                callback=self.ticker_callback

            )



            # candle 1분봉

            self.ws.kline_stream(

                interval=1,

                symbol=DEFAULT_SYMBOL,

                callback=self.kline_callback

            )



            print("[PUBLIC WS STARTED]")



            while self.running:

                time.sleep(1)



        except Exception as e:


            print(
                "[PUBLIC WS START ERROR]",
                e
            )



    # ======================================
    # THREAD
    # ======================================

    def run_thread(self):


        thread = threading.Thread(

            target=self.start,

            daemon=True

        )


        thread.start()



    # ======================================
    # STOP
    # ======================================

    def stop(self):


        self.running = False


        print(
            "[PUBLIC WS STOPPED]"
        )



    # ======================================
    # GET PRICE
    # ======================================

    def get_price(self):

        return self.price



    # ======================================
    # GET CANDLES
    # ======================================

    def get_prices(self):

        return self.kline.copy()



# ==========================================
# SINGLETON
# ==========================================

public_ws = PublicWS()
