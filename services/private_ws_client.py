import time
import json
import hmac
import hashlib
import websocket


from config import (
    BYBIT_PRIVATE_WS,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
)


from position.position_manager import position_manager



class PrivateWSClient:


    def __init__(self):

        self.url = BYBIT_PRIVATE_WS

        self.api_key = BYBIT_API_KEY

        self.api_secret = BYBIT_API_SECRET


        self.ws = None

        self.running = False

        self.authenticated = False


        print("==============================")
        print("[PRIVATE WS CLIENT INIT]")
        print("URL :", self.url)
        print("KEY :", self.api_key[:6])
        print("==============================")



    # ==================================
    # SIGN
    # ==================================

    def sign(
        self,
        expires
    ):


        param = (
            "GET/realtime"
            +
            str(expires)
        )


        return hmac.new(

            self.api_secret.encode(
                "utf-8"
            ),

            param.encode(
                "utf-8"
            ),

            hashlib.sha256

        ).hexdigest()



    # ==================================
    # OPEN
    # ==================================

    def on_open(
        self,
        ws
    ):


        print(
            "[PRIVATE CONNECTED]"
        )


        expires = int(
            time.time()*1000
        ) + 10000



        signature = self.sign(
            expires
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



    # ==================================
    # MESSAGE
    # ==================================

    def on_message(
        self,
        ws,
        message
    ):


        try:


            data = json.loads(
                message
            )



            # AUTH RESULT

            if data.get("op") == "auth":


                if data.get("success"):


                    self.authenticated = True


                    print(
                        "[PRIVATE AUTH SUCCESS]"
                    )


                    self.subscribe(
                        ws
                    )


                else:


                    print(
                        "[PRIVATE AUTH FAILED]",
                        data
                    )


                return




            topic = data.get(
                "topic",
                ""
            )



            if topic.startswith(
                "order"
            ):


                print(
                    "[ORDER UPDATE]"
                )


                position_manager.sync()



            elif topic.startswith(
                "position"
            ):


                print(
                    "[POSITION UPDATE]"
                )


                position_manager.sync()



        except Exception as e:


            print(
                "[PRIVATE MESSAGE ERROR]",
                e
            )



    # ==================================
    # SUBSCRIBE
    # ==================================

    def subscribe(
        self,
        ws
    ):


        msg = {


            "op":
                "subscribe",


            "args":

                [

                    "order",

                    "position"

                ]

        }



        ws.send(
            json.dumps(msg)
        )


        print(
            "[PRIVATE SUBSCRIBED]"
        )



    # ==================================
    # ERROR
    # ==================================

    def on_error(
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

    def on_close(
        self,
        ws,
        code,
        msg
    ):


        print(
            "[PRIVATE WS CLOSED]",
            code,
            msg
        )


        self.authenticated = False



    # ==================================
    # START
    # ==================================

    def start(self):


        if self.running:

            return


        self.running = True


        print(
            "[PRIVATE WS START]"
        )


        while self.running:


            try:


                self.ws = websocket.WebSocketApp(

                    self.url,

                    on_open=self.on_open,

                    on_message=self.on_message,

                    on_error=self.on_error,

                    on_close=self.on_close

                )



                self.ws.run_forever(

                    ping_interval=20,

                    ping_timeout=10

                )



            except Exception as e:


                print(
                    "[PRIVATE LOOP ERROR]",
                    e
                )



            if self.running:


                print(
                    "[PRIVATE RECONNECT]"
                )


                time.sleep(5)



    # ==================================
    # STOP
    # ==================================

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




private_ws_client = PrivateWSClient()
