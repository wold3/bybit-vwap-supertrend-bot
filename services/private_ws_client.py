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

        self.ws = None

        self.running = False

        self.thread = None


        print("==============================")
        print("[PRIVATE WS CLIENT INIT]")
        print("URL :", self.url)
        print("KEY :", BYBIT_API_KEY[:6])
        print("==============================")



    # ==================================
    # SIGN
    # ==================================

    def _auth_sign(self):

        expires = int(
            (time.time()+10)*1000
        )


        origin = (
            "GET/realtime"
            +
            str(expires)
        )


        sign = hmac.new(

            BYBIT_API_SECRET.encode(),

            origin.encode(),

            hashlib.sha256

        ).hexdigest()


        return expires, sign



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


        print(
            "[PRIVATE WS START]"
        )


        self.ws = websocket.WebSocketApp(

            self.url,

            on_open=self._on_open,

            on_message=self._on_message,

            on_error=self._on_error,

            on_close=self._on_close

        )


        self.ws.run_forever()



    # ==================================
    # OPEN
    # ==================================

    def _on_open(self, ws):


        print(
            "[PRIVATE CONNECTED]"
        )


        expires, sign = self._auth_sign()



        auth = {

            "op":"auth",

            "args":[

                BYBIT_API_KEY,

                expires,

                sign

            ]

        }


        ws.send(
            json.dumps(auth)
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



            if data.get("op") == "auth":


                if data.get("success"):

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


                if topic == "order":


                    print(
                        "[ORDER EVENT]",
                        data["data"]
                    )



                elif topic == "execution":


                    print(
                        "[EXECUTION EVENT]",
                        data["data"]
                    )



                elif topic == "position":


                    print(
                        "[POSITION EVENT]",
                        data["data"]
                    )



                elif topic == "wallet":


                    print(
                        "[WALLET EVENT]",
                        data["data"]
                    )



        except Exception as e:


            print(
                "[PRIVATE PARSE ERROR]",
                e
            )





    # ==================================
    # SUBSCRIBE
    # ==================================

    def subscribe(self, ws):


        payload = {


            "op":

            "subscribe",


            "args":

            [

                "order",

                "execution",

                "position",

                "wallet"

            ]

        }


        ws.send(

            json.dumps(payload)

        )


        print(
            "[PRIVATE SUBSCRIBED]"
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
            "[PRIVATE WS ERROR]",
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
            "[PRIVATE WS CLOSED]"
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
            "[PRIVATE WS CLIENT STOPPED]"
        )





private_ws_client = PrivateWSClient()
