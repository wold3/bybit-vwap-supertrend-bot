import time
import json
import hmac
import hashlib
import threading
import websocket


from config import (
    BYBIT_PRIVATE_WS,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    DEFAULT_SYMBOL
)


from position.position_manager import position_manager





class PrivateWSClient:



    def __init__(self):


        self.url = BYBIT_PRIVATE_WS

        self.api_key = BYBIT_API_KEY

        self.api_secret = BYBIT_API_SECRET


        self.ws = None


        self.running = True


        self.authenticated = False





        print("==============================")
        print("[PRIVATE WS CLIENT INIT]")
        print("URL :", self.url)
        print("KEY :", self.api_key[:6])
        print("==============================")







    # ==============================
    # SIGN
    # ==============================


    def sign(self, expires):


        payload = (
            "GET/realtime"
            +
            str(expires)
        )


        return hmac.new(

            bytes(
                self.api_secret,
                "utf-8"
            ),

            payload.encode(
                "utf-8"
            ),

            hashlib.sha256

        ).hexdigest()







    # ==============================
    # OPEN
    # ==============================


    def on_open(self, ws):


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









    # ==============================
    # MESSAGE
    # ==============================


    def on_message(
            self,
            ws,
            message
    ):


        try:


            data = json.loads(
                message
            )



            print(
                "[PRIVATE DATA]",
                data.get("topic")
            )







            # AUTH

            if data.get("op") == "auth":


                if data.get("success"):


                    self.authenticated = True


                    print(
                        "[PRIVATE AUTH SUCCESS]"
                    )



                    self.subscribe(ws)



                return







            topic = data.get(
                "topic",
                ""
            )






            # ORDER UPDATE


            if topic.startswith(
                "order"
            ):


                print(
                    "[ORDER UPDATE]",
                    data
                )



                position_manager.sync()






            # POSITION UPDATE


            if topic.startswith(
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







    # ==============================
    # SUBSCRIBE
    # ==============================


    def subscribe(
            self,
            ws
    ):


        args = [


            "order",


            "position"

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







    # ==============================
    # CLOSE
    # ==============================


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







    def on_error(
            self,
            ws,
            error
    ):


        print(
            "[PRIVATE WS ERROR]",
            error
        )







    # ==============================
    # START
    # ==============================


    def start(self):


        print(
            "[PRIVATE WS START]"
        )



        while self.running:



            try:


                self.ws = websocket.WebSocketApp(

                    self.url,

                    on_open=self.on_open,

                    on_message=self.on_message,

                    on_close=self.on_close,

                    on_error=self.on_error

                )



                self.ws.run_forever()



            except Exception as e:


                print(
                    "[PRIVATE RECONNECT ERROR]",
                    e
                )



            time.sleep(5)







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
