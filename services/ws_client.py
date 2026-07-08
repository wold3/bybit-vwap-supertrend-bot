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


    def __init__(self):


        self.url = os.getenv(

            "BYBIT_PUBLIC_WS",

            "wss://stream-testnet.bybit.com/v5/public/linear"

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
    # LOOP
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



                self.ws.run_forever(

                    ping_interval=20,

                    ping_timeout=10

                )



            except Exception as e:


                print(

                    "[PUBLIC WS ERROR]",

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



        subscribe = {


            "op":

                "subscribe",


            "args":

                [

                    "publicTrade."

                    +

                    self.symbol

                ]

        }



        ws.send(

            json.dumps(

                subscribe

            )

        )



        print(

            "[PUBLIC SUBSCRIBED]",

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



            topic = data.get(

                "topic"

            )



            if topic != (

                "publicTrade."

                +

                self.symbol

            ):


                return



            trades = data.get(

                "data",

                []

            )



            for trade in trades:


                price = float(

                    trade.get(

                        "p"

                    )

                )


                volume = float(

                    trade.get(

                        "v"

                    )

                )



                symbol = trade.get(

                    "s"

                )



                candle_builder.update(

                    symbol,

                    price,

                    volume

                )



                candle = candle_builder.get_latest(

                    symbol

                )



                if candle:


                    self.process_candle(

                        candle

                    )





        except Exception as e:


            print(

                "[MESSAGE ERROR]",

                e

            )





    # =====================================
    # CANDLE PROCESS
    # =====================================

    def process_candle(
        self,
        candle
    ):


        indicator_engine.update(

            candle

        )


        indicators = indicator_engine.calculate()



        market_data = {


            **candle,


            **indicators

        }



        self.latest_data = market_data


        self.last_update = time.time()





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

            "[PUBLIC WS CLOSED]"

        )





    # =====================================
    # STOP
    # =====================================

    def stop(self):


        self.running = False


        self.connected = False



        if self.ws:


            self.ws.close()





    # =====================================
    # DATA
    # =====================================

    def get_latest_data(
        self
    ):


        return self.latest_data





    def status(
        self
    ):


        return {


            "running":

                self.running,


            "connected":

                self.connected,


            "latest":

                self.latest_data

        }





ws_client = WSClient()
