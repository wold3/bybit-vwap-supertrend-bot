# =====================================================
# services/private_ws.py
# Bybit Private WebSocket
# =====================================================

import time
import json
import hmac
import hashlib
import threading
import websocket


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_WS_URL,
    CATEGORY,
    DEFAULT_SYMBOL
)





class PrivateWS:


    def __init__(self):


        self.running = False

        self.ws = None

        self.thread = None


        print(
            "[PRIVATE WS READY]"
        )








    # =====================================================
    # AUTH SIGN
    # =====================================================


    def sign(self):


        expires = int(

            (time.time()+5)*1000

        )


        param = (

            "GET/realtime"

            +

            str(expires)

        )



        signature = hmac.new(

            BYBIT_API_SECRET.encode(),

            param.encode(),

            hashlib.sha256

        ).hexdigest()



        return [

            "auth",

            BYBIT_API_KEY,

            expires,

            signature

        ]









    # =====================================================
    # START
    # =====================================================


    def start(self):


        if self.running:

            return



        self.running = True



        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )


        self.thread.start()








    # =====================================================
    # RUN
    # =====================================================


    def run(self):


        while self.running:


            try:


                print(

                    "[PRIVATE WS CONNECTING]"

                )



                self.ws = websocket.WebSocketApp(

                    BYBIT_WS_URL + "/v5/private",

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



            time.sleep(5)









    # =====================================================
    # OPEN
    # =====================================================


    def on_open(
        self,
        ws
    ):


        print(

            "[PRIVATE WS CONNECTED]"

        )



        ws.send(

            json.dumps(

                {

                    "op":

                    "auth",


                    "args":

                    self.sign()

                }

            )

        )









    # =====================================================
    # MESSAGE
    # =====================================================


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

                "op"

            ) == "auth":



                print(

                    "[PRIVATE WS AUTH OK]"

                )



                ws.send(

                    json.dumps(

                        {

                            "op":

                            "subscribe",


                            "args":

                            [

                                "position",

                                "order",

                                "execution"

                            ]

                        }

                    )

                )



                print(

                    "[PRIVATE WS SUBSCRIBED]"

                )



            else:


                print(

                    "[PRIVATE WS DATA]",

                    data.get("topic")

                )



        except Exception as e:


            print(

                "[WS PARSE ERROR]",

                e

            )









    # =====================================================
    # ERROR
    # =====================================================


    def on_error(
        self,
        ws,
        error
    ):


        print(

            "[PRIVATE WS ERROR]",

            error

        )









    # =====================================================
    # CLOSE
    # =====================================================


    def on_close(
        self,
        ws,
        code,
        msg
    ):


        print(

            "[PRIVATE WS CLOSED]"

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

            "[PRIVATE WS STOPPED]"

        )








# =====================================================
# INSTANCE
# =====================================================


private_ws = PrivateWS()
