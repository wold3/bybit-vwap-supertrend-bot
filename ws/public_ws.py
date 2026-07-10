import threading
import time

from pybit.unified_trading import WebSocket

from config import (
    BYBIT_TESTNET,
    CATEGORY,
    DEFAULT_SYMBOL,
)


# ==========================================
# BYBIT PUBLIC WEBSOCKET V5
# ==========================================

class PublicWS:


    def __init__(self):

        self.ws = None

        self.running = False

        self.last_price = None

        self.kline = []


        print("==============================")
        print("[PUBLIC WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")



    # ======================================
    # PRICE CALLBACK
    # ======================================

    def handle_ticker(self, message):

        try:

            data = message.get("data")


            if not data:
                return


            price = data.get("lastPrice")


            if price:

                self.last_price = float(price)



        except Exception as e:

            print(
                "[PUBLIC TICKER ERROR]",
                e
            )



    # ======================================
    # KLINE CALLBACK
    # ======================================

    def handle_kline(self, message):

        try:

            data = message.get("data")


            if not data:
                return


            for candle in data:


                item = {

                    "start": candle.get("start"),

                    "open": float(candle.get("open")),

                    "high": float(candle.get("high")),

                    "low": float(candle.get("low")),

                    "close": float(candle.get("close")),

                    "volume": float(candle.get("volume"))

                }


                self.kline.append(item)



            # 최근 200개 유지

            if len(self.kline) > 200:

                self.kline = self.kline[-200:]



        except Exception as e:

            print(
                "[PUBLIC KLINE ERROR]",
                e
            )



    # ======================================
    # START
    # ======================================

    def start(self):


        if self.running:

            return


        self.running = True



        self.ws = WebSocket(

            testnet=BYBIT_TESTNET,

            channel_type="linear"

        )



        # 실시간 가격

        self.ws.ticker_stream(

            symbol=DEFAULT_SYMBOL,

            callback=self.handle_ticker

        )



        # 1분봉

        self.ws.kline_stream(

            interval=1,

            symbol=DEFAULT_SYMBOL,

            callback=self.handle_kline

        )



        print("[PUBLIC WS STARTED]")



        while self.running:

            time.sleep(1)



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


        print("[PUBLIC WS STOPPED]")



    # ======================================
    # GETTERS
    # ======================================

    def get_price(self):

        return self.last_price



    def get_candles(self):

        return self.kline





# ==========================================
# SINGLETON
# ==========================================

public_ws = PublicWS()
