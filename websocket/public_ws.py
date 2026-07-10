import json
import threading
import time

from websocket import WebSocketApp

from config import (
    BYBIT_PUBLIC_WS,
    CATEGORY,
    DEFAULT_SYMBOL,
)



# ==========================================
# BYBIT PUBLIC WEBSOCKET
# ==========================================


class PublicWS:



    def __init__(self):

        self.ws = None

        self.running = False

        self.thread = None


        self.candles = []


        print("==============================")
        print("[PUBLIC WS INIT]")
        print("URL :", BYBIT_PUBLIC_WS)
        print("SYMBOL :", DEFAULT_SYMBOL)
        print("==============================")





    # ======================================
    # START
    # ======================================

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






    # ======================================
    # CONNECT
    # ======================================

    def _run(self):


        while self.running:


            try:


                self.ws = WebSocketApp(

                    BYBIT_PUBLIC_WS,

                    on_open=self.on_open,

                    on_message=self.on_message,

                    on_error=self.on_error,

                    on_close=self.on_close

                )



                self.ws.run_forever()



            except Exception as e:


                print(
                    "[PUBLIC WS ERROR]",
                    e
                )



            time.sleep(3)







    # ======================================
    # OPEN
    # ======================================

    def on_open(
        self,
        ws
    ):


        topic = (

            "kline.1."

            +

            DEFAULT_SYMBOL

        )


        request = {


            "op":
            "subscribe",


            "args":
            [
                topic
            ]

        }



        ws.send(

            json.dumps(request)

        )


        print(
            "[PUBLIC WS CONNECTED]"
        )







    # ======================================
    # MESSAGE
    # ======================================

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





            for item in data["data"]:



                candle = {


                    "start":
                    item["start"],


                    "open":
                    float(
                        item["open"]
                    ),


                    "high":
                    float(
                        item["high"]
                    ),


                    "low":
                    float(
                        item["low"]
                    ),


                    "close":
                    float(
                        item["close"]
                    ),


                    "volume":
                    float(
                        item["volume"]
                    )

                }




                self.candles.append(
                    candle
                )



                if len(self.candles) > 200:


                    self.candles.pop(0)




        except Exception as e:


            print(
                "[WS MESSAGE ERROR]",
                e
            )







    # ======================================
    # ERROR
    # ======================================

    def on_error(

        self,

        ws,

        error

    ):


        print(
            "[PUBLIC WS ERROR]",
            error
        )







    # ======================================
    # CLOSE
    # ======================================

    def on_close(

        self,

        ws,

        code,

        msg

    ):


        print(
            "[PUBLIC WS CLOSED]"
        )







    # ======================================
    # GET CANDLES
    # ======================================

    def get_candles(self):

        return self.candles







    # ======================================
    # STOP
    # ======================================

    def stop(self):


        self.running = False



        if self.ws:


            self.ws.close()



        print(
            "[PUBLIC WS STOP]"
        )






# ==========================================
# SINGLETON
# ==========================================

public_ws = PublicWS()
