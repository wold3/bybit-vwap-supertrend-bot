import time
import threading

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

        self.ticker = None

        self.kline = []

        print("==============================")
        print("[PUBLIC WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")



    # ======================================
    # TICKER CALLBACK
    # ======================================

    def handle_ticker(self, message):

        try:

            self.ticker = message


        except Exception as e:

            print(
                "[TICKER CALLBACK ERROR]",
                e
            )



    # ======================================
    # KLINE CALLBACK
    # ======================================

    def handle_kline(self, message):

        try:

            data = message.get(
                "data",
                []
            )


            for candle in data:

                self.kline.append(candle)



            if len(self.kline) > 500:

                self.kline = self.kline[-500:]



        except Exception as e:

            print(
                "[KLINE CALLBACK ERROR]",
                e
            )



    # ======================================
    # START
    # ======================================

    def start(self):

        try:


            self.running = True



            # IMPORTANT
            # Demo Trading Public WS 사용 금지
            # Public Market Data = 일반 V5 endpoint

            self.ws = WebSocket(

                testnet=BYBIT_TESTNET,

                channel_type="linear"

            )



            self.ws.ticker_stream(

                symbol=DEFAULT_SYMBOL,

                callback=self.handle_ticker

            )



            self.ws.kline_stream(

                symbol=DEFAULT_SYMBOL,

                interval=1,

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



    # ======================================
    # THREAD START
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


        try:

            if self.ws:

                self.ws.exit()

        except:

            pass



        print(
            "[PUBLIC WS STOPPED]"
        )



    # ======================================
    # PRICE GETTER
    # ======================================

    def get_price(self):

        try:

            if not self.ticker:

                return None



            data = self.ticker.get(
                "data",
                {}
            )



            price = data.get(
                "lastPrice"
            )



            if price:

                return float(price)



        except Exception as e:

            print(
                "[PRICE ERROR]",
                e
            )



        return None



    # ======================================
    # KLINE GETTER
    # ======================================

    def get_kline(self):

        return self.kline





# ==========================================
# SINGLETON
# ==========================================

public_ws = PublicWS()
