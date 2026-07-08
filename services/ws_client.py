# services/ws_client.py

import os
import json
import time
import threading

import websocket

from dotenv import load_dotenv


from market.candle_builder import candle_builder

from indicators.indicator_engine import indicator_engine

from watchdog.watchdog import watchdog



load_dotenv()



class WSClient:
    """
    Bybit Public WebSocket Client

    기능:
    - Market Tick 수신
    - Candle 생성
    - Indicator 업데이트
    - Strategy 데이터 제공
    """



    def __init__(self):


        self.url = (

            "wss://stream.bybit.com/v5/public/linear"

        )


        self.symbol = os.getenv(

            "DEFAULT_SYMBOL",

            "BTCUSDT"

        )


        self.running = False

        self.connected = False

        self.ws = None

        self.thread = None


        self.latest_data = None


        self.last_update = 0





    # =====================================
    # START
    # =====================================

    def start(self):


        if self.running:

            return



        self.running = True



        self.thread = threading.Thread(

            target=self._run,

            daemon=True

        )


        self.thread.start()



        print(

            "[PUBLIC WS START]"

        )





    # =====================================
    # CONNECT LOOP
    # =====================================

    def _run(self):


        while self.running:


            try:


                self.ws = websocket.WebSocketApp(

                    self.url,

                    on_open=self.on_open,

                    on_message=self.on_message,

                    on_error=self.on_error,

                    on_close=self.on_close

                )



                self.ws.run_forever()



            except Exception as e:


                print(

                    "[WS LOOP ERROR]",

                    e

                )



            time.sleep(5)





    # =====================================
    # OPEN
    # =====================================

    def on_open(
        self,
        ws
    ):


        self.connected = True



        payload = {


            "op":

                "subscribe",


            "args":

                [

                    f"tickers.{self.symbol}"

                ]

        }



        ws.send(

            json.dumps(payload)

        )



        print(

            "[WS CONNECTED]",

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



            watchdog.heartbeat()



            if "data" not in data:

                return



            topic = data.get(

                "topic",

                ""

            )



            if (

                topic.startswith(

                    "tickers."

                )

            ):



                self.handle_ticker(

                    data["data"]

                )



        except Exception as e:


            print(

                "[WS MESSAGE ERROR]",

                e

            )





    # =====================================
    # TICKER HANDLER
    # =====================================

    def handle_ticker(
        self,
        data
    ):


        try:


            symbol = data.get(

                "symbol"

            )



            last_price = float(

                data.get(

                    "lastPrice"

                )

            )



            volume = float(

                data.get(

                    "volume24h",

                    0

                )

            )



            # Tick 전달

            candle_builder.update(

                symbol,

                last_price,

                volume

            )



            candle = candle_builder.close_candle(

                symbol

            )



            if candle:



                indicator_engine.update(

                    candle

                )


                indicators = indicator_engine.calculate()



                market_data = {


                    **candle,


                    **indicators


                }



                self.update_market_data(

                    market_data

                )



        except Exception as e:


            print(

                "[TICK ERROR]",

                e

            )





    # =====================================
    # DATA UPDATE
    # =====================================

    def update_market_data(
        self,
        data
    ):


        self.latest_data = data


        self.last_update = time.time()





    # =====================================
    # GET DATA
    # =====================================

    def get_latest_data(
        self
    ):


        return self.latest_data





    # =====================================
    # ERROR
    # =====================================

    def on_error(
        self,
        ws,
        error
    ):


        print(

            "[WS ERROR]",

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


        self.connected = False


        print(

            "[WS CLOSED]"

        )





    # =====================================
    # STOP
    # =====================================

    def stop(self):


        self.running = False


        self.connected = False



        try:

            if self.ws:

                self.ws.close()


        except:

            pass





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "running":

                self.running,


            "connected":

                self.connected,


            "symbol":

                self.symbol,


            "has_data":

                self.latest_data is not None,


            "last_update":

                self.last_update

        }





ws_client = WSClient()
