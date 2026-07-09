import json
import threading
import time

import websocket

from config import (
    DEFAULT_SYMBOL,
    BYBIT_PUBLIC_WS,
)



class PublicWebSocketClient:


    def __init__(self):

        self.symbol = DEFAULT_SYMBOL

        self.url = BYBIT_PUBLIC_WS

        self.ws = None

        self.running = False

        self.thread = None

        self.callback = None


        print("==============================")
        print("[PUBLIC WS INIT]")
        print("URL :", self.url)
        print("SYMBOL :", self.symbol)
        print("==============================")



    # =====================================================
    # CALLBACK
    # =====================================================

    def set_callback(self, callback):

        self.callback = callback



    # =====================================================
    # START
    # =====================================================

    def start(self):

        if self.running:

            return


        self.running = True


        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )


        self.thread.start()



    # =====================================================
    # LOOP
    # =====================================================

    def _run(self):


        while self.running:


            try:


                print(
                    "[PUBLIC WS CONNECTING]",
                    self.url
                )


                self.ws = websocket.WebSocketApp(

                    self.url,

                    on_open=self._on_open,

                    on_message=self._on_message,

                    on_error=self._on_error,

                    on_close=self._on_close

                )


                self.ws.run_forever(

                    ping_interval=20,

                    ping_timeout=10

                )



            except Exception as e:


                print(
                    "[PUBLIC WS LOOP ERROR]",
                    e
                )



            if self.running:


                print(
                    "[PUBLIC WS RECONNECT]"
                )


                time.sleep(5)




    # =====================================================
    # OPEN
    # =====================================================

    def _on_open(
        self,
        ws
    ):


        print(
            "[PUBLIC WS CONNECTED]"
        )


        payload = {


            "op":
            "subscribe",


            "args":

            [

                f"kline.1.{self.symbol}"

            ]

        }


        ws.send(
            json.dumps(payload)
        )


        print(
            "[PUBLIC WS SUBSCRIBED]",
            self.symbol
        )



    # =====================================================
    # MESSAGE
    # =====================================================

    def _on_message(
        self,
        ws,
        message
    ):


        try:


            data = json.loads(
                message
            )


        except:


            return



        if "topic" not in data:

            return



        if not data["topic"].startswith(
            "kline"
        ):

            return



        candles = data.get(
            "data",
            []
        )



        for c in candles:


            try:


                candle = {


                    "symbol":
                    self.symbol,


                    "timestamp":
                    int(c["start"]),


                    "open":
                    float(c["open"]),


                    "high":
                    float(c["high"]),


                    "low":
                    float(c["low"]),


                    "close":
                    float(c["close"]),


                    "volume":
                    float(c["volume"]),


                    "confirm":
                    bool(
                        c.get(
                            "confirm",
                            False
                        )
                    )

                }



                if self.callback:


                    self.callback(
                        candle
                    )



            except Exception as e:


                print(
                    "[CANDLE ERROR]",
                    e
                )



    # =====================================================
    # ERROR
    # =====================================================

    def _on_error(
        self,
        ws,
        error
    ):


        print(
            "[PUBLIC WS ERROR]",
            error
        )



    # =====================================================
    # CLOSE
    # =====================================================

    def _on_close(
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



    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        self.running = False


        try:

            if self.ws:

                self.ws.close()


        except:

            pass


        print(
            "[PUBLIC WS STOPPED]"
        )





ws_client = PublicWebSocketClient()
