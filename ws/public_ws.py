import threading
import time


from pybit.unified_trading import WebSocket


from config import (
    BYBIT_TESTNET,
    CATEGORY,
    DEFAULT_SYMBOL,
)





# ==========================================
# PUBLIC WS MANAGER
# ==========================================

class PublicWS:


    def __init__(self):


        self.ws = None


        self.running = False


        self.thread = None



        self.price = 0



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

    def handle_kline(self, message):


        try:


            data = message.get(
                "data",
                []
            )


            if not data:

                return



            candle = data[0]



            close = float(

                candle["close"]

            )


            self.price = close




            print(
                "[KLINE]",
                close
            )





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

                close

            )


            self.volumes.append(

                float(
                    candle["volume"]
                )

            )




            # memory limit

            max_len = 200



            if len(self.closes) > max_len:


                self.opens.pop(0)

                self.highs.pop(0)

                self.lows.pop(0)

                self.closes.pop(0)

                self.volumes.pop(0)





        except Exception as e:


            print(
                "[KLINE ERROR]",
                e
            )





    # ======================================
    # CONNECT
    # ======================================

    def connect(self):


        self.ws = WebSocket(


            testnet=BYBIT_TESTNET,


            channel_type=CATEGORY

        )



        self.ws.kline_stream(


            interval="1",


            symbol=DEFAULT_SYMBOL,


            callback=self.handle_kline

        )



        print(
            "[PUBLIC WS STARTED]"
        )





        while self.running:


            time.sleep(1)





    # ======================================
    # START LOOP
    # ======================================

    def start(self):


        self.running = True



        while self.running:



            try:


                self.connect()



            except Exception as e:


                print(
                    "[PUBLIC WS ERROR]",
                    e
                )



                print(
                    "[PUBLIC WS RECONNECT] 5 sec"
                )


                time.sleep(5)





    # ======================================
    # THREAD
    # ======================================

    def run_thread(self):


        self.thread = threading.Thread(


            target=self.start,


            daemon=True

        )


        self.thread.start()





    # ======================================
    # STOP
    # ======================================

    def stop(self):


        self.running = False



        print(
            "[PUBLIC WS STOPPED]"
        )





    # ======================================
    # DATA ACCESS
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
