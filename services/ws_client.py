import os
import json
import time
import websocket
import threading


from dotenv import load_dotenv


from watchdog.watchdog import watchdog



load_dotenv()





class BybitPublicWS:


    def __init__(self):


        self.url = os.getenv(

            "PUBLIC_WS_URL",

            "wss://stream.bybit.com/v5/public/linear"

        )



        self.symbol = os.getenv(

            "DEFAULT_SYMBOL",

            "BTCUSDT"

        )



        self.interval = "1"



        self.latest_data = {}



        self.lock = threading.Lock()





    # =====================================
    # OPEN
    # =====================================

    def on_open(
        self,
        ws
    ):


        print(

            "📡 PUBLIC WS CONNECTED"

        )



        ws.send(json.dumps({

            "op":

                "subscribe",


            "args":

                [

                    "kline."

                    +

                    self.interval

                    +

                    "."

                    +

                    self.symbol

                ]

        }))



        print(

            "PUBLIC CHANNEL SUBSCRIBED"

        )





    # =====================================
    # MESSAGE
    # =====================================

    def on_message(
        self,
        ws,
        message
    ):


        try:


            data = json.loads(

                message

            )



            topic = data.get(

                "topic"

            )



            if (

                topic

                and

                topic.startswith(

                    "kline"

                )

            ):


                self.handle_kline(

                    data

                )



                watchdog.update_public_ws()



        except Exception as e:


            print(

                "PUBLIC WS ERROR",

                e

            )





    # =====================================
    # KLINE
    # =====================================

    def handle_kline(
        self,
        data
    ):


        candles = data.get(

            "data",

            []

        )



        if not candles:

            return



        candle = candles[0]



        with self.lock:


            self.latest_data = {


                "symbol":

                    self.symbol,


                "open":

                    float(

                        candle["open"]

                    ),


                "high":

                    float(

                        candle["high"]

                    ),


                "low":

                    float(

                        candle["low"]

                    ),


                "close":

                    float(

                        candle["close"]

                    ),


                "volume":

                    float(

                        candle["volume"]

                    ),


                "timestamp":

                    candle["start"]


            }



    # =====================================
    # GET DATA
    # =====================================

    def get_latest_data(
        self
    ):


        with self.lock:


            return self.latest_data.copy()





    # =====================================
    # ERROR
    # =====================================

    def on_error(
        self,
        ws,
        error
    ):


        print(

            "PUBLIC WS ERROR",

            error

        )





    # =====================================
    # CLOSE
    # =====================================

    def on_close(
        self,
        ws,
        code,
        msg
    ):


        print(

            "PUBLIC WS CLOSED"

        )





    # =====================================
    # START
    # =====================================

    def start(self):


        while True:


            try:


                ws = websocket.WebSocketApp(

                    self.url,


                    on_open=self.on_open,


                    on_message=self.on_message,


                    on_error=self.on_error,


                    on_close=self.on_close

                )



                ws.run_forever()



            except Exception as e:


                print(

                    "PUBLIC RECONNECT",

                    e

                )



            time.sleep(5)





ws_client = BybitPublicWS()
