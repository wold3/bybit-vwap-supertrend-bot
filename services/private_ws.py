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



class PrivateWS:


    def __init__(self):

        self.url = BYBIT_PRIVATE_WS

        self.api_key = BYBIT_API_KEY

        self.api_secret = BYBIT_API_SECRET


        self.ws = None

        self.running = False

        self.thread = None


        self.authenticated = False


        print("==============================")
        print("[PRIVATE WS INIT]")
        print("URL :", self.url)
        print("KEY :", self.api_key[:6])
        print("==============================")



    # =================================
    # START
    # =================================

    def start(self):

        if self.running:

            return


        self.running = True


        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )


        self.thread.start()



    # =================================
    # STOP
    # =================================

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



    # =================================
    # RUN
    # =================================

    def run(self):


        self.ws = websocket.WebSocketApp(

            self.url,


            on_open=self.on_open,


            on_message=self.on_message,


            on_error=self.on_error,


            on_close=self.on_close

        )


        self.ws.run_forever()



    # =================================
    # AUTH SIGN
    # =================================

    def _auth_signature(self):


        expires = (
            int(time.time()*1000)
            +
            10000
        )


        payload = (
            "GET/realtime"
            +
            str(expires)
        )


        sign = hmac.new(

            self.api_secret.encode(),

            payload.encode(),

            hashlib.sha256

        ).hexdigest()



        return (
            expires,
            sign
        )



    # =================================
    # OPEN
    # =================================

    def on_open(
        self,
        ws
    ):


        print(
            "[PRIVATE CONNECTED]"
        )


        expires, sign = (
            self._auth_signature()
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



    # =================================
    # MESSAGE
    # =================================

    def on_message(
        self,
        ws,
        message
    ):


        try:


            data = json.loads(
                message
            )


            if data.get("op") == "auth":


                if data.get("success"):


                    self.authenticated = True


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



    # =================================
    # SUBSCRIBE
    # =================================

    def subscribe(
        self,
        ws
    ):


        args = [

            "position",

            "execution",

            "order",

            "wallet"

        ]


        msg = {


            "op":
                "subscribe",


            "args":
                args

        }


        ws.send(
            json.dumps(msg)
        )


        print(
            "[PRIVATE SUBSCRIBED]"
        )



    # =================================
    # ERROR
    # =================================

    def on_error(
        self,
        ws,
        error
    ):


        print(
            "[PRIVATE WS ERROR]",
            error
        )



    # =================================
    # CLOSE
    # =================================

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



private_ws = PrivateWS()
