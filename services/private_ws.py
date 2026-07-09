# services/private_ws.py

import json
import time
import hmac
import hashlib
import threading
import websocket


from config import (
    BYBIT_PRIVATE_WS,
    BYBIT_API_KEY,
    BYBIT_API_SECRET
)



class PrivateWS:


    def __init__(self):


        self.url = BYBIT_PRIVATE_WS


        self.api_key = BYBIT_API_KEY


        self.api_secret = BYBIT_API_SECRET


        self.ws = None


        self.running = False


        self.thread = None



        print("==============================")
        print("[PRIVATE WS INIT]")
        print("URL :", self.url)
        print("KEY :", self.api_key[:6] if self.api_key else None)
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
            "[PRIVATE WS STOPPED]"
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
                    "[PRIVATE WS ERROR]",
                    e
                )



            if self.running:


                print(
                    "[PRIVATE WS RECONNECT]"
                )


                time.sleep(3)




    # =====================================
    # AUTH SIGN
    # =====================================

    def generate_signature(
        self,
        expires
    ):


        payload = (
            "GET/realtime"
            +
            str(expires)
        )



        signature = hmac.new(

            self.api_secret.encode(),

            payload.encode(),

            hashlib.sha256

        ).hexdigest()



        return signature



    # =====================================
    # OPEN
    # =====================================

    def on_open(
        self,
        ws
    ):


        print(
            "[PRIVATE CONNECTED]"
        )



        expires = (
            int(time.time() * 1000)
            +
            10000
        )



        sign = self.generate_signature(
            expires
        )



        auth = {


            "op":
                "auth",


            "args":
            [

                self.api_key,

                expires,

                sign

            ]

        }



        ws.send(
            json.dumps(auth)
        )



        time.sleep(1)



        subscribe = {


            "op":
                "subscribe",


            "args":
            [

                "position",

                "execution",

                "order"

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



            if data.get(
                "success"
            ):


                print(
                    "[PRIVATE AUTH SUCCESS]"
                )


                return



            topic = data.get(
                "topic",
                ""
            )



            if topic:


                print(
                    "[PRIVATE DATA]",
                    topic
                )



        except Exception as e:


            print(
                "[PRIVATE MESSAGE ERROR]",
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
            "[PRIVATE WS ERROR]",
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
            "[PRIVATE WS CLOSED]"
        )





private_ws = PrivateWS()
