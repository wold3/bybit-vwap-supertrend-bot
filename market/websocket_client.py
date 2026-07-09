import json
import time
import threading
import websocket


from config import (
    BYBIT_PUBLIC_WS,
    DEFAULT_SYMBOL
)



class MarketWebSocketClient:


    def __init__(self):


        self.url = BYBIT_PUBLIC_WS

        self.symbol = DEFAULT_SYMBOL


        self.ws = None

        self.thread = None

        self.running = False


        self.candles = []



        print("==============================")
        print("[PUBLIC WS INIT]")
        print("URL :", self.url)
        print("SYMBOL :", self.symbol)
        print("==============================")



    # ===============================
    # START
    # ===============================

    def start(self):


        if self.running:


            print(
                "[PUBLIC WS ALREADY RUNNING]"
            )


            return



        self.running = True



        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )


        self.thread.start()



    # ===============================
    # STOP
    # ===============================

    def stop(self):


        self.running = False



        if self.ws:


            try:

                self.ws.close()

            except:

                pass



        print(
            "[PUBLIC WS STOPPED]"
        )



    # ===============================
    # RUN
    # ===============================

    def run(self):


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
                    "[PUBLIC LOOP ERROR]",
                    e
                )



            if self.running:


                print(
                    "[PUBLIC RECONNECT]"
                )


                time.sleep(3)



    # ===============================
    # OPEN
    # ===============================

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

            json.dumps(subscribe)

        )



        print(
            "[PUBLIC SUBSCRIBED]"
        )



    # ===============================
    # MESSAGE
    # ===============================

    def on_message(
        self,
        ws,
        message
    ):


        try:


            data = json.loads(
                message
            )



            if "topic" not in data:

                return



            if not data["topic"].startswith(
                "kline"
            ):

                return



            rows = data.get(
                "data",
                []
            )



            for row in rows:


                candle = {


                    "symbol":

                        self.symbol,


                    "timestamp":

                        row["start"],


                    "open":

                        float(row["open"]),


                    "high":

                        float(row["high"]),


                    "low":

                        float(row["low"]),


                    "close":

                        float(row["close"]),


                    "volume":

                        float(row["volume"])

                }



                self.candles.append(
                    candle
                )



                if len(self.candles) > 500:


                    self.candles.pop(0)



                print(
                    "[LAST CANDLE]",
                    candle
                )



        except Exception as e:


            print(
                "[PUBLIC MESSAGE ERROR]",
                e
            )



    # ===============================
    # ERROR
    # ===============================

    def on_error(
        self,
        ws,
        error
    ):


        print(
            "[PUBLIC WS ERROR]",
            error
        )



    # ===============================
    # CLOSE
    # ===============================

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





ws_client = MarketWebSocketClient()
