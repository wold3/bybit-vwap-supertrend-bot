import threading
import time

from pybit.unified_trading import WebSocket

from config import (
    BYBIT_TESTNET,
    DEFAULT_SYMBOL,
    CATEGORY,
)


# ==========================================
# BYBIT PUBLIC WEBSOCKET V5
# ==========================================

class PublicWS:


    def __init__(self):

        self.ws = None

        self.running = False

        self.kline = None

        self.ticker = None

        self.orderbook = None


        print("==============================")
        print("[PUBLIC WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")



    # ======================================
    # CALLBACK
    # ======================================

    def handle_message(self, message):

        try:

            topic = message.get("topic")


            # ------------------------------
            # KLINE
            # ------------------------------

            if topic.startswith("kline"):

                self.kline = message



            # ------------------------------
            # TICKER
            # ------------------------------

            elif topic.startswith("tickers"):

                self.ticker = message



            # ------------------------------
            # ORDERBOOK
            # ------------------------------

            elif topic.startswith("orderbook"):

                self.orderbook = message



        except Exception as e:

            print(
                "[PUBLIC WS ERROR]",
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



        # 1분봉

        self.ws.kline_stream(

            interval=1,

            symbol=DEFAULT_SYMBOL,

            callback=self.handle_message

        )



        # Ticker

        self.ws.ticker_stream(

            symbol=DEFAULT_SYMBOL,

            callback=self.handle_message

        )



        # Orderbook

        self.ws.orderbook_stream(

            depth=50,

            symbol=DEFAULT_SYMBOL,

            callback=self.handle_message

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

    def get_kline(self):

        return self.kline



    def get_ticker(self):

        return self.ticker



    def get_orderbook(self):

        return self.orderbook





# ==========================================
# SINGLETON
# ==========================================

public_ws = PublicWS()
