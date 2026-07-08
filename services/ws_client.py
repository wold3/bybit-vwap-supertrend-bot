import os
import json
import time
import threading
import traceback

import websocket
from dotenv import load_dotenv


from market.candle_builder import candle_builder
from indicators.indicator_engine import indicator_engine
from watchdog.watchdog import watchdog


load_dotenv()



class WSClient:


    def __init__(self):


        self.symbol = os.getenv(
            "DEFAULT_SYMBOL",
            "BTCUSDT"
        )


        live = (
            os.getenv(
                "LIVE_TRADING",
                "false"
            )
            .lower()
            ==
            "true"
        )


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



        self.running = False

        self.connected = False

        self.ws = None

        self.thread = None


        self.latest_data = None

        self.last_update = 0





    # ================================
    # START
    # ================================

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





    # ================================
    # WS LOOP
    # ================================

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


            except Exception:


                traceback.print_exc()



            if self.running:

                time.sleep(5)






    # ================================
    # OPEN
    # ================================

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

                    f"publicTrade.{self.symbol}"

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







    # ================================
    # MESSAGE
    # ================================

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



            if data.get("topic") != f"publicTrade.{self.symbol}":

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




                # 현재 진행중 캔들도 사용

                current = (
                    candle_builder.current.get(
                        symbol
                    )
                )


                if current:

                    candle = current.copy()


                elif candles:

                    candle = candles[-1]


                else:

                    continue





                print(
                    "[LAST CANDLE]",
                    candle
                )



                self.process_market(
                    candle
                )



        except Exception as e:


            print(
                "[MESSAGE ERROR]",
                e
            )


            traceback.print_exc()






    # ================================
    # PROCESS
    # ================================

    def process_market(
        self,
        candle
    ):


        try:


            indicator_engine.update(
                candle
            )



            indicators = indicator_engine.calculate(

                candle["symbol"]

            )



            print(
                "[INDICATORS]",
                indicators
            )



            self.latest_data = {


                **candle,


                **indicators

            }


            self.last_update = time.time()



        except Exception as e:


            print(
                "[PROCESS ERROR]",
                e
            )







    # ================================
    # ERROR
    # ================================

    def on_error(
        self,
        ws,
        error
    ):


        print(
            "[PUBLIC WS ERROR]",
            error
        )






    # ================================
    # CLOSE
    # ================================

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






    # ================================
    # STOP
    # ================================

    def stop(self):


        self.running = False


        self.connected = False



        if self.ws:


            try:

                self.ws.close()

            except:

                pass



        print(
            "[PUBLIC WS STOPPED]"
        )







    # ================================
    # DATA
    # ================================

    def get_latest_data(self):

        return self.latest_data





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
