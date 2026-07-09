# market/websocket_client.py

import json
import time
import threading
import websocket


from config import (
    BYBIT_PUBLIC_WS,
    DEFAULT_SYMBOL
)



class WebSocketClient:


    def __init__(self):


        self.url = BYBIT_PUBLIC_WS


        self.symbol = DEFAULT_SYMBOL


        self.ws = None


        self.running = False


        self.thread = None


        self.latest_price = None


        self.last_update = 0



        print("==============================")
        print("[MARKET WS INIT]")
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
            "[MARKET WS STOPPED]"
        )



    # =====================================
    # RUN
    # =====================================

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
                    "[MARKET WS ERROR]",
                    e
                )



            if self.running:


                print(
                    "[MARKET WS RECONNECT]"
                )


                time.sleep(3)




    # =====================================
    # OPEN
    # =====================================

    def on_open(
        self,
        ws
    ):


        print(
            "[MARKET WS CONNECTED]"
        )



        subscribe = {


            "op":
                "subscribe",


            "args":
            [

                f"tickers.{self.symbol}"

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



            if topic.startswith(
                "tickers."
            ):


                ticker = data["data"]



                price = ticker.get(
                    "lastPrice"
                )



                if price:


                    self.latest_price = float(
                        price
                    )


                    self.last_update = time.time()



                    print(

                        "[PRICE]",

                        self.symbol,

                        self.latest_price

                    )



        except Exception as e:


            print(
                "[MARKET MESSAGE ERROR]",
                e
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
            "[MARKET WS ERROR]",
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
            "[MARKET WS CLOSED]"
        )



    # =====================================
    # GET PRICE
    # =====================================

    def get_price(
        self
    ):


        return self.latest_price




websocket_client = WebSocketClient()
