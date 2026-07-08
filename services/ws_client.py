import json
import time
import threading
import requests
import websocket


from config import DEFAULT_SYMBOL


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


        self.candles = []



    # =====================================
    # START
    # =====================================

    def start(self):


        self.load_initial_candles()


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
            "[PUBLIC WS CLOSED]"
        )



    # =====================================
    # INITIAL CANDLE LOAD
    # =====================================

    def load_initial_candles(self):


        try:


            url = (
                "https://api.bybit.com/v5/market/kline"
            )


            params = {

                "category": "linear",

                "symbol": self.symbol,

                "interval": "1",

                "limit": "500"

            }



            response = requests.get(

                url,

                params=params,

                timeout=5

            )



            data = response.json()



            if data.get("retCode") != 0:


                print(
                    "[KLINE LOAD ERROR]",
                    data
                )

                return



            rows = (
                data["result"]["list"]
            )


            rows.reverse()



            self.candles.clear()



            for row in rows:


                candle = {


                    "symbol":
                        self.symbol,


                    "timestamp":
                        int(row[0]),


                    "open":
                        float(row[1]),


                    "high":
                        float(row[2]),


                    "low":
                        float(row[3]),


                    "close":
                        float(row[4]),


                    "volume":
                        float(row[5])

                }


                self.candles.append(
                    candle
                )



            print(
                "[INITIAL CANDLES]",
                len(self.candles)
            )



        except Exception as e:


            print(
                "[INITIAL CANDLE ERROR]",
                e
            )



    # =====================================
    # CONNECT
    # =====================================

    def run(self):


        url = (
            "wss://stream.bybit.com/v5/public/linear"
        )


        while self.running:


            try:


                self.ws = websocket.WebSocketApp(

                    url,

                    on_open=self.on_open,

                    on_message=self.on_message,

                    on_error=self.on_error,

                    on_close=self.on_close

                )


                self.ws.run_forever()



            except Exception as e:


                print(
                    "[WS RECONNECT ERROR]",
                    e
                )



            if self.running:


                time.sleep(3)



    # =====================================
    # OPEN
    # =====================================

    def on_open(self, ws):


        print(
            "[PUBLIC WS CONNECTED]"
        )


        subscribe = {


            "op":
                "subscribe",


            "args":[

                f"kline.1.{self.symbol}"

            ]

        }


        ws.send(
            json.dumps(subscribe)
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


                self.process_market(
                    candle
                )



        except Exception as e:


            print(
                "[WS MESSAGE ERROR]",
                e
            )



    # =====================================
    # MARKET PROCESS
    # =====================================

    def process_market(
        self,
        candle
    ):



        market_data = {


            "symbol":
                self.symbol,


            "timestamp":
                int(candle["start"]),


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



        # candle update

        if self.candles:


            if self.candles[-1]["timestamp"] == market_data["timestamp"]:


                self.candles[-1] = market_data


            else:


                self.candles.append(
                    market_data
                )


        else:


            self.candles.append(
                market_data
            )



        if len(self.candles) > 500:


            self.candles.pop(0)



        print(
            "[CANDLE COUNT]",
            len(self.candles)
        )



        # ===============================
        # STRATEGY
        # ===============================

        try:


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


        except Exception as e:


            print(
                "[STRATEGY ERROR]",
                e
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
