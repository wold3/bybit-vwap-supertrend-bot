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



        self.prices = []


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
    # TICKER CALLBACK
    # ======================================

    def ticker_callback(

        self,

        message

    ):


        try:


            data = message.get(

                "data",

                {}

            )


            if "lastPrice" in data:


                price = float(

                    data["lastPrice"]

                )


                self.prices.append(

                    price

                )


                if len(self.prices) > 500:

                    self.prices.pop(0)



                print(

                    "[PRICE]",

                    price

                )



        except Exception as e:


            print(
                "[TICKER ERROR]",
                e
            )





    # ======================================
    # KLINE CALLBACK
    # ======================================

    def kline_callback(

        self,

        message

    ):


        try:


            data = message.get(

                "data",

                []

            )


            if not data:

                return




            candle = data[0]



            self.opens.append(

                float(

                    candle["open"]

                )

            )


            self.highs.append(

                float(

                    candle["high"]

                )

            )


            self.lows.append(

                float(

                    candle["low"]

                )

            )


            self.closes.append(

                float(

                    candle["close"]

                )

            )


            self.volumes.append(

                float(

                    candle["volume"]

                )

            )



            if len(self.closes) > 500:


                self.opens.pop(0)

                self.highs.pop(0)

                self.lows.pop(0)

                self.closes.pop(0)

                self.volumes.pop(0)




            print(

                "[KLINE]",

                self.closes[-1]

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



            self.ws.ticker_stream(

                symbol=DEFAULT_SYMBOL,

                callback=self.ticker_callback

            )



            self.ws.kline_stream(

                interval=1,

                symbol=DEFAULT_SYMBOL,

                callback=self.kline_callback

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
    # DATA GETTER
    # ======================================

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
