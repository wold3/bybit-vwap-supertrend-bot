# services/private_ws_client.py

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



class PrivateWSClient:


    def __init__(self):


        self.url = BYBIT_PRIVATE_WS


        self.api_key = BYBIT_API_KEY


        self.api_secret = BYBIT_API_SECRET


        self.ws = None


        self.running = False


        self.thread = None


        self.authenticated = False



        print("==============================")
        print("[PRIVATE WS CLIENT INIT]")
        print("URL :", self.url)
        print(
            "KEY :",
            self.api_key[:6]
            if self.api_key
            else None
        )
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
            "[PRIVATE WS CLIENT STOPPED]"
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
                    "[PRIVATE CLIENT ERROR]",
                    e
                )



            if self.running:


                print(
                    "[PRIVATE WS RECONNECT]"
                )


                time.sleep(3)




    # =====================================
    # SIGN
    # =====================================

    def create_signature(
        self,
        expires
    ):


        payload = (

            "GET/realtime"

            +

            str(expires)

        )



        signature = hmac.new(

            self.api_secret.encode(
                "utf-8"
            ),

            payload.encode(
                "utf-8"
            ),

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

            int(
                time.time() * 1000
            )

            +

            10000

        )



        signature = self.create_signature(
            expires
        )



        auth_message = {


            "op":
                "auth",


            "args":
            [

                self.api_key,

                expires,

                signature

            ]

        }



        ws.send(
            json.dumps(auth_message)
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


                self.authenticated = True


                print(
                    "[PRIVATE AUTH SUCCESS]"
                )



                self.subscribe(ws)



                return



            topic = data.get(
                "topic"
            )



            if topic:


                print(
                    "[PRIVATE EVENT]",
                    topic
                )



        except Exception as e:


            print(
                "[PRIVATE MESSAGE ERROR]",
                e
            )



    # =====================================
    # SUBSCRIBE
    # =====================================

    def subscribe(
        self,
        ws
    ):


        payload = {


            "op":
                "subscribe",


            "args":
            [

                "order",

                "execution",

                "position"

            ]

        }



        ws.send(
            json.dumps(payload)
        )



        print(
            "[PRIVATE SUBSCRIBED]"
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


        self.authenticated = False


        print(
            "[PRIVATE WS CLOSED]"
        )





private_ws_client = PrivateWSClient()
