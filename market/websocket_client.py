import json
import time
import threading
import websocket


from config import (
    DEFAULT_SYMBOL,
    BYBIT_PUBLIC_WS
)


from strategy.vwap_supertrend_strategy import (
    vwap_supertrend_strategy
)


from execution.order_manager import (
    order_manager
)



class WebSocketClient:


    def __init__(self):


        self.symbol = DEFAULT_SYMBOL


        self.url = BYBIT_PUBLIC_WS


        self.ws = None


        self.running = False


        self.thread = None


        self.latest_data = None


        self.last_update = 0


        self.candles = []



        print("==============================")
        print("[PUBLIC WS INIT]")
        print("URL :", self.url)
        print("SYMBOL :", self.symbol)
        print("==============================")



    # =====================================
    # START
    # =====================================

    def start(self):


        if self.running:

            return


        self.running = True


        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )


        self.thread.start()



    # =====================================
    # STOP
    # =====================================

    def stop(self):


        self.running = False


        try:

            if self.ws:

                self.ws.close()


        except Exception:


            pass



        print(
            "[PUBLIC WS STOPPED]"
        )



    # =====================================
    # CONNECT
    # =====================================

    def run(self):


        self.ws = websocket.WebSocketApp(

            self.url,


            on_open=self.on_open,


            on_message=self.on_message,


            on_error=self.on_error,


            on_close=self.on_close

        )


        self.ws.run_forever()



    # =====================================
    # OPEN
    # =====================================

    def on_open(
        self,
        ws
    ):


        print(
            "[PUBLIC WS CONNECTED]"
        )



        subscribe = {


            "op":
                "subscribe",


            "args":

                [

                    f"kline.1.{self.symbol}"

                ]

        }



        ws.send(
            json.dumps(
                subscribe
            )
        )



        print(
            "[PUBLIC SUBSCRIBED]"
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


            if "data" not in data:

                return



            topic = data.get(
                "topic",
                ""
            )



            if "kline" not in topic:

                return



            for candle in data["data"]:


                self.process_candle(
                    candle
                )



        except Exception as e:


            print(
                "[PUBLIC WS MESSAGE ERROR]",
                e
            )



    # =====================================
    # CANDLE PROCESS
    # =====================================

    def process_candle(
        self,
        candle
    ):



        market = {


            "symbol":
                self.symbol,


            "timestamp":
                int(
                    candle["start"]
                ),


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
                )

        }



        self.latest_data = market


        self.last_update = time.time()



        # candle update

        if self.candles:


            if (
                self.candles[-1]["timestamp"]
                ==
                market["timestamp"]
            ):


                self.candles[-1] = market



            else:


                self.candles.append(
                    market
                )


        else:


            self.candles.append(
                market
            )



        # keep 500

        if len(self.candles) > 500:

            self.candles.pop(0)



        print(
            "[CANDLE COUNT]",
            len(self.candles)
        )



        # strategy

        signal = (
            vwap_supertrend_strategy.analyze(
                self.candles
            )
        )


        if signal:


            print(
                "[SIGNAL]",
                signal
            )


            order_manager.execute(
                signal
            )



        print(
            "[LAST CANDLE]",
            market
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


        print(
            "[PUBLIC WS CLOSED]",
            code,
            msg
        )



    # =====================================
    # DATA
    # =====================================

    def get_latest_data(self):


        return self.latest_data




ws_client = WebSocketClient()
