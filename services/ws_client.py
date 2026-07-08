import os
import json
import time
import threading

import websocket

from dotenv import load_dotenv


from market.candle_builder import (
    candle_builder
)


from indicators.indicator_engine import (
    indicator_engine
)


from strategy.vwap_supertrend_strategy import (
    vwap_supertrend_strategy
)


from execution.order_manager import (
    order_manager
)


from watchdog.watchdog import (
    watchdog
)



load_dotenv()



class WSClient:


    def __init__(self):


        live = os.getenv(
            "LIVE_TRADING",
            "false"
        ).lower() == "true"



        if live:

            self.url = os.getenv(
                "BYBIT_LIVE_PUBLIC_WS",
                "wss://stream.bybit.com/v5/public/linear"
            )


        else:

            self.url = os.getenv(
                "BYBIT_DEMO_PUBLIC_WS",
                "wss://stream-demo.bybit.com/v5/public/linear"
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

                    "publicTrade."

                    +

                    self.symbol

                ]

        }



        ws.send(

            json.dumps(payload)

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



            if data.get("topic") != (

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

                    trade["p"]

                )



                volume = float(

                    trade["v"]

                )



                symbol = trade.get(

                    "s",

                    self.symbol

                )



                print(

                    "[TICK]",

                    symbol,

                    price,

                    volume

                )





                candle_builder.update(

                    symbol,

                    price,

                    volume

                )





                candles = candle_builder.get_candles(

                    symbol

                )





                print(

                    "[CANDLE COUNT]",

                    symbol,

                    len(candles)

                )





                current = candle_builder.current.get(

                    symbol

                )



                if current:


                    print(

                        "[LAST CANDLE]",

                        current

                    )





                self.process_market(

                    symbol

                )





        except Exception as e:


            print(

                "[MESSAGE ERROR]",

                e

            )







    # =====================================
    # MARKET PROCESS
    # =====================================

    def process_market(
        self,
        symbol
    ):


        candles = candle_builder.get_candles(

            symbol

        )



        current = candle_builder.current.get(

            symbol

        )



        if current:

            candles = candles + [

                current

            ]



        if len(candles) < 2:

            return





        candle = candles[-1]



        print(

            "[LAST CANDLE]",

            candle

        )





        indicator_engine.update(

            candle

        )





        indicators = indicator_engine.calculate(

            symbol

        )





        print(

            "[INDICATORS]",

            indicators

        )






        market_data = {


            "symbol":

                candle["symbol"],


            "timestamp":

                candle["timestamp"],


            "open":

                candle["open"],


            "high":

                candle["high"],


            "low":

                candle["low"],


            "close":

                candle["close"],


            "volume":

                candle["volume"],


            **indicators

        }





        self.latest_data = market_data


        self.last_update = time.time()





        # =====================================
        # STRATEGY
        # =====================================


        signal = vwap_supertrend_strategy.analyze(

            candles

        )



        if signal:


            print(

                "[STRATEGY SIGNAL]",

                signal

            )



            order_manager.execute(

                signal

            )








    # =====================================
    # ERROR
    # =====================================

    def on_error(
        self,
        ws,
        error
    ):


        print(

            "[PUBLIC WS ERROR]",

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


            try:

                self.ws.close()


            except:


                pass







    # =====================================
    # DATA
    # =====================================

    def get_latest_data(
        self
    ):


        return self.latest_data







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


            "last_update":

                self.last_update,


            "latest":

                self.latest_data

        }





ws_client = WSClient()
