import json
import time
import hmac
import hashlib
import threading
import websocket


from config import (
    BYBIT_PRIVATE_WS,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
)



class PrivateWSClient:


    def __init__(self):

        self.url = BYBIT_PRIVATE_WS

        self.api_key = BYBIT_API_KEY

        self.api_secret = BYBIT_API_SECRET


        self.ws = None

        self.thread = None

        self.running = False


        self.auth_done = False

        self.subscribed = False



        print("==============================")
        print("[PRIVATE WS CLIENT INIT]")
        print("URL :", self.url)
        print("KEY :", self.api_key[:6])
        print("==============================")



    # ===============================
    # START
    # ===============================

    def start(self):


        if self.running:

            print(
                "[PRIVATE WS ALREADY RUNNING]"
            )

            return


        self.running = True


        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )


        self.thread.start()



        print(
            "[PRIVATE WS START]"
        )



    # ===============================
    # STOP
    # ===============================

    def stop(self):


        self.running = False


        self.auth_done = False

        self.subscribed = False



        if self.ws:


            try:

                self.ws.close()


            except Exception:

                pass



        print(
            "[PRIVATE WS CLIENT STOPPED]"
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
                    "[PRIVATE LOOP ERROR]",
                    e
                )



            if self.running:


                print(
                    "[PRIVATE RECONNECT]"
                )


                time.sleep(3)



    # ===============================
    # SIGN
    # ===============================

    def create_signature(self):


        expires = (

            int(time.time()*1000)

            +

            10000

        )


        param = (
            "GET/realtime"
            +
            str(expires)
        )



        signature = hmac.new(

            self.api_secret.encode(),

            param.encode(),

            hashlib.sha256

        ).hexdigest()



        return expires, signature



    # ===============================
    # OPEN
    # ===============================

    def on_open(
        self,
        ws
    ):


        print(
            "[PRIVATE CONNECTED]"
        )


        self.auth_done = False

        self.subscribed = False



        expires, signature = (
            self.create_signature()
        )



        auth = {


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
            json.dumps(auth)
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



            # AUTH

            if data.get("op") == "auth":


                if data.get("success"):


                    if not self.auth_done:


                        self.auth_done = True


                        print(
                            "[PRIVATE AUTH SUCCESS]"
                        )


                        self.subscribe(ws)



                else:


                    print(
                        "[PRIVATE AUTH FAILED]",
                        data
                    )


                return



            # SUB RESPONSE

            if data.get("op") == "subscribe":


                if data.get("success"):


                    if not self.subscribed:


                        self.subscribed = True


                        print(
                            "[PRIVATE SUBSCRIBED]"
                        )


                return



            if "topic" in data:


                print(
                    "[PRIVATE DATA]",
                    data["topic"]
                )



        except Exception as e:


            print(
                "[PRIVATE MESSAGE ERROR]",
                e
            )



    # ===============================
    # SUBSCRIBE
    # ===============================

    def subscribe(
        self,
        ws
    ):


        if self.subscribed:

            return



        msg = {


            "op":
                "subscribe",


            "args":

                [

                    "wallet",

                    "position",

                    "execution",

                    "order"

                ]

        }



        ws.send(
            json.dumps(msg)
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
            "[PRIVATE ERROR]",
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


        self.auth_done = False

        self.subscribed = False



        print(
            "[PRIVATE WS CLOSED]"
        )





private_ws_client = PrivateWSClient()
