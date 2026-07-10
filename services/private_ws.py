# =====================================================
# services/private_ws.py
# Bybit Private WebSocket V5
# =====================================================

import json
import time
import hmac
import hashlib
import threading
import websocket



from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    BYBIT_PRIVATE_WS
)


from portfolio.position_manager import (
    position_manager
)







class PrivateWebSocket:



    def __init__(self):


        self.ws = None


        self.running = False


        self.connected = False


        self.thread = None



        print(

            "[PRIVATE WS READY]"

        )







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



        print(

            "[PRIVATE WS CONNECTING]"

        )







    # =====================================================
    # AUTH
    # =====================================================

    def create_auth(self):


        expires = int(

            time.time()*1000

        ) + 10000



        signature = hmac.new(

            BYBIT_API_SECRET.encode(),

            (

                "GET/realtime"

                +

                str(expires)

            ).encode(),

            hashlib.sha256

        ).hexdigest()



        return {


            "op":

                "auth",


            "args":

                [

                    BYBIT_API_KEY,

                    expires,

                    signature

                ]

        }







    # =====================================================
    # RUN
    # =====================================================

    def run(self):


        while self.running:


            try:


                self.ws = websocket.WebSocketApp(

                    BYBIT_PRIVATE_WS,

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


        self.connected = True



        print(

            "[PRIVATE WS CONNECTED]"

        )



        ws.send(

            json.dumps(

                self.create_auth()

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



            if data.get("success"):


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

                                    "execution",

                                    "order"

                                ]

                        }

                    )

                )



                print(

                    "[PRIVATE WS SUBSCRIBED]"

                )



                return





            topic = data.get(

                "topic"

            )



            if topic == "position":


                print(

                    "[POSITION EVENT]"

                )


                position_manager.sync()



            elif topic == "execution":


                print(

                    "[EXECUTION EVENT]"

                )


                position_manager.sync()



            elif topic == "order":


                print(

                    "[ORDER EVENT]"

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


        self.connected = False



        print(

            "[PRIVATE WS CLOSED]"

        )







    # =====================================================
    # STATUS
    # =====================================================

    def status(self):


        return {


            "running":

                self.running,


            "connected":

                self.connected


        }







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
# SINGLETON
# =====================================================

private_ws = PrivateWebSocket()
