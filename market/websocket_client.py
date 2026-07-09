import json
import time
import threading
import websocket


from config import DEFAULT_SYMBOL




class PublicWebSocketClient:


    def __init__(self):

        self.symbol = DEFAULT_SYMBOL

        self.url = (
            "wss://stream.bybit.com/v5/public/linear"
        )


        self.ws = None

        self.running = False

        self.thread = None


        self.callback = None



        print("==============================")
        print("[PUBLIC WS INIT]")
        print("URL :", self.url)
        print("SYMBOL :", self.symbol)
        print("==============================")




    # ==================================
    # CALLBACK
    # ==================================

    def set_callback(
        self,
        callback
    ):

        self.callback = callback





    # ==================================
    # START
    # ==================================

    def start(self):


        if self.running:

            return



        self.running = True



        self.thread = threading.Thread(

            target=self._run,

            daemon=True

        )


        self.thread.start()





    def _run(self):


        while self.running:


            try:


                self.ws = websocket.WebSocketApp(

                    self.url,

                    on_open=self._on_open,

                    on_message=self._on_message,

                    on_error=self._on_error,

                    on_close=self._on_close

                )


                self.ws.run_forever()



            except Exception as e:


                print(
                    "[PUBLIC WS ERROR]",
                    e
                )



            if self.running:


                print(
                    "[PUBLIC RECONNECT]"
                )


                time.sleep(3)







    # ==================================
    # OPEN
    # ==================================

    def _on_open(
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






    # ==================================
    # MESSAGE
    # ==================================

    def _on_message(
        self,
        ws,
        message
    ):


        try:


            data = json.loads(
                message
            )



            topic = data.get(
                "topic"
            )



            if not topic:

                return



            if not topic.startswith(
                "kline"
            ):

                return





            candles = data.get(
                "data",
                []
            )



            for c in candles:



                candle = {


                    "symbol":

                    self.symbol,


                    "timestamp":

                    c.get("start"),


                    "open":

                    float(c.get("open")),


                    "high":

                    float(c.get("high")),


                    "low":

                    float(c.get("low")),


                    "close":

                    float(c.get("close")),


                    "volume":

                    float(c.get("volume"))

                }




                print(
                    "[CANDLE]",
                    candle
                )





                if self.callback:


                    self.callback(
                        candle
                    )




        except Exception as e:


            print(
                "[PUBLIC PARSE ERROR]",
                e
            )







    # ==================================
    # ERROR
    # ==================================

    def _on_error(
        self,
        ws,
        error
    ):


        print(
            "[PUBLIC WS ERROR]",
            error
        )







    # ==================================
    # CLOSE
    # ==================================

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







    # ==================================
    # STOP
    # ==================================

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
