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

        self.kline = []

        self.last_price = None


        print("==============================")
        print("[PUBLIC WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")



    # ======================================
    # KLINE CALLBACK
    # ======================================

    def handle_kline(self, message):

        try:

            data = message.get("data")


            if not data:
                return


            for candle in data:

                close = float(
                    candle["close"]
                )


                self.last_price = close


                self.kline.append(
                    candle
                )


                # 최근 200개 유지

                if len(self.kline) > 200:

                    self.kline.pop(0)



                print(
                    "[KLINE]",
                    close
                )



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
    # DATA GETTER
    # ======================================

    def get_prices(self):


        prices = []


        for candle in self.kline:

            try:

                prices.append(

                    float(
                        candle["close"]
                    )

                )

            except:

                pass



        return prices



    def get_last_price(self):

        return self.last_price




# ==========================================
# SINGLETON
# ==========================================

public_ws = PublicWS()
