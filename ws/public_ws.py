import threading
import time


from pybit.unified_trading import WebSocket


from config import (

    BYBIT_TESTNET,

    BYBIT_DEMO,

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


            high = float(

                candle["high"]

            )


            low = float(

                candle["low"]

            )


            open_price = float(

                candle["open"]

            )


            volume = float(

                candle["volume"]

            )





            self.opens.append(

                open_price

            )


            self.highs.append(

                high

            )


            self.lows.append(

                low

            )


            self.closes.append(

                close

            )


            self.volumes.append(

                volume

            )





            # 최대 보관

            limit = 200



            if len(self.closes) > limit:


                self.opens.pop(0)

                self.highs.pop(0)

                self.lows.pop(0)

                self.closes.pop(0)

                self.volumes.pop(0)





            print(

                "[KLINE]",

                close

            )





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


            demo=BYBIT_DEMO,


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
                    "[PUBLIC WS RECONNECT] 5 SEC"
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
    # OHLCV
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
