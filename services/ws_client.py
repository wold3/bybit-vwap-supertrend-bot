import json
import time
import threading
import websocket


from config import (
    DEFAULT_SYMBOL
)


from strategy.vwap_supertrend_strategy import (
    vwap_supertrend_strategy
)


from execution.order_manager import (
    order_manager
)



class WSClient:


    def __init__(self):


        self.symbol = DEFAULT_SYMBOL


        self.ws = None


        self.running = False


        self.thread = None



        self.latest_data = None


        self.last_update = 0



        # candle storage

        self.candles = []



    # =====================================
    # START
    # =====================================

    def start(self):


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


        except:

            pass



        print(
            "[PUBLIC WS CLOSED]"
        )



    # =====================================
    # CONNECT
    # =====================================

    def run(self):


        url = (
            "wss://stream.bybit.com/v5/public/linear"
        )


        self.ws = websocket.WebSocketApp(

            url,

            on_open=self.on_open,

            on_message=self.on_message,

            on_error=self.on_error,

            on_close=self.on_close

        )


        self.ws.run_forever()



    # =====================================
    # OPEN
    # =====================================

    def on_open(self, ws):


        print(
            "[PUBLIC WS CONNECTED]"
        )


        sub = {

            "op":"subscribe",

            "args":[

                f"kline.1.{self.symbol}"

            ]

        }


        ws.send(
            json.dumps(sub)
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



            if "kline" in topic:


                for candle in data["data"]:


                    self.process_market(
                        candle
                    )



        except Exception as e:


            print(
                "[WS MESSAGE ERROR]",
                e
            )



    # =====================================
    # PROCESS MARKET
    # =====================================

    def process_market(
        self,
        candle
    ):



        market_data = {


            "symbol":
                self.symbol,


            "timestamp":
                candle["start"],


            "open":
                float(candle["open"]),


            "high":
                float(candle["high"]),


            "low":
                float(candle["low"]),


            "close":
                float(candle["close"]),


            "volume":
                float(candle["volume"])

        }



        self.latest_data = market_data


        self.last_update = time.time()



        # ===============================
        # CANDLE BUFFER
        # ===============================


        if self.candles:


            if (
                self.candles[-1]["timestamp"]
                ==
                market_data["timestamp"]
            ):


                self.candles[-1] = market_data


            else:


                self.candles.append(
                    market_data
                )


        else:


            self.candles.append(
                market_data
            )



        # keep 500 candles

        if len(self.candles) > 500:


            self.candles.pop(0)



        print(
            "[CANDLE COUNT]",
            len(self.candles)
        )



        # ===============================
        # STRATEGY
        # ===============================


        signal = vwap_supertrend_strategy.analyze(

            self.candles

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
            market_data
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


        print(
            "[PUBLIC WS CLOSED]"
        )



    # =====================================
    # GET DATA
    # =====================================

    def get_latest_data(self):


        return self.latest_data





ws_client = WSClient()
