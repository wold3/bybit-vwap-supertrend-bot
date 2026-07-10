import threading
import time


from pybit.unified_trading import WebSocket


from config import (
    BYBIT_PUBLIC_WS,
    CATEGORY,
    DEFAULT_SYMBOL,
    BYBIT_TESTNET,
)



# ==========================================
# PUBLIC KLINE WEBSOCKET
# ==========================================

class PublicWS:


    def __init__(self):


        self.ws = None

        self.running = False


        self.price = None


        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.volumes = []



        print("==============================")
        print("[PUBLIC WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")




    # ======================================
    # KLINE CALLBACK
    # ======================================

    def handle_kline(
        self,
        message
    ):


        try:


            data = message.get(
                "data"
            )


            if not data:

                return



            candle = data[0]



            open_price = float(
                candle["open"]
            )

            high_price = float(
                candle["high"]
            )

            low_price = float(
                candle["low"]
            )

            close_price = float(
                candle["close"]
            )

            volume = float(
                candle["volume"]
            )



            self.price = close_price



            self.opens.append(
                open_price
            )

            self.highs.append(
                high_price
            )

            self.lows.append(
                low_price
            )

            self.closes.append(
                close_price
            )

            self.volumes.append(
                volume
            )



            if len(self.closes) > 300:


                self.opens = self.opens[-300:]

                self.highs = self.highs[-300:]

                self.lows = self.lows[-300:]

                self.closes = self.closes[-300:]

                self.volumes = self.volumes[-300:]



            print(
                "[KLINE]",
                close_price
            )



        except Exception as e:


            print(
                "[KLINE ERROR]",
                e
            )




    # ======================================
    # START
    # ======================================

    def start(self):


        try:


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
    # GETTERS
    # ======================================

    def get_price(self):

        return self.price



    def get_ohlcv(self):


        return (

            self.opens,

            self.highs,

            self.lows,

            self.closes,

            self.volumes

        )





# ==========================================
# SINGLETON
# ==========================================

public_ws = PublicWS()
