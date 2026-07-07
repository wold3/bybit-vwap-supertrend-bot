import os
import json
import time
import threading
import websocket

from dotenv import load_dotenv

from watchdog.watchdog import watchdog

from indicators.indicator_engine import indicator_engine


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


        self.interval = os.getenv(

            "KLINE_INTERVAL",

            "1"

        )


        self.latest_data = {}


        self.lock = threading.Lock()





    # =====================================
    # CONNECT
    # =====================================

    def on_open(
        self,
        ws
    ):


        print(
            "📡 PUBLIC WS CONNECTED"
        )



        subscribe = {


            "op":

                "subscribe",


            "args":

                [

                    f"kline.{self.interval}.{self.symbol}"

                ]

        }



        ws.send(

            json.dumps(

                subscribe

            )

        )


        print(

            "PUBLIC SUBSCRIBED",

            self.symbol

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



            if not topic:

                return



            if topic.startswith(

                "kline"

            ):


                self.handle_kline(

                    data

                )


                watchdog.update_public_ws()



        except Exception as e:


            print(

                "WS MESSAGE ERROR",

                e

            )





    # =====================================
    # KLINE 처리
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



        # Bybit kline

        formatted = {


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





        # =================================
        # Indicator Engine 연결
        # =================================

        indicator_engine.update(

            formatted

        )





        # =================================
        # 최신 데이터 저장
        # =================================

        with self.lock:


            self.latest_data = formatted.copy()





            indicators = (

                indicator_engine
                .calculate()

            )



            self.latest_data.update(

                indicators

            )





    # =====================================
    # STRATEGY DATA
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

            "PUBLIC WS CLOSED",

            code,

            msg

        )





    # =====================================
    # START
    # =====================================

    def start(
        self
    ):


        while True:


            try:


                ws = websocket.WebSocketApp(

                    self.url,

                    on_open=self.on_open,

                    on_message=self.on_message,

                    on_error=self.on_error,

                    on_close=self.on_close

                )



                ws.run_forever(

                    ping_interval=20,

                    ping_timeout=10

                )



            except Exception as e:


                print(

                    "PUBLIC WS RECONNECT ERROR",

                    e

                )



            time.sleep(5)





ws_client = BybitPublicWS()
