# =====================================================
# services/private_ws.py
# Bybit Private WebSocket V5
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
    BYBIT_PRIVATE_WS
)


from portfolio.position_manager import (
    position_manager
)





class PrivateWS:



    def __init__(self):


        self.running = False


        self.connected = False


        self.ws = None


        self.thread = None


        self.lock = threading.Lock()



        print(

            "[PRIVATE WS READY]"

        )









    # =====================================================
    # AUTH SIGN
    # =====================================================

    def generate_signature(self):


        expires = str(

            int(time.time()*1000)

            +

            10000

        )


        payload = (

            "GET/realtime"

            +

            expires

        )


        signature = hmac.new(

            BYBIT_API_SECRET.encode(),

            payload.encode(),

            hashlib.sha256

        ).hexdigest()



        return [

            "GET",

            expires,

            signature

        ]









    # =====================================================
    # START
    # =====================================================

    def start(self):


        with self.lock:


            if self.running:


                return



            self.running = True



        print(

            "[PRIVATE WS CONNECTING]"

        )



        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )



        self.thread.start()









    # =====================================================
    # LOOP
    # =====================================================

    def run(self):


        while self.running:


            try:


                self.connect()



            except Exception as e:


                print(

                    "[PRIVATE WS ERROR]",

                    e

                )



            if self.running:


                time.sleep(5)









    # =====================================================
    # CONNECT
    # =====================================================

    def connect(self):


        self.ws = websocket.WebSocketApp(

            BYBIT_PRIVATE_WS,


            on_open=self.on_open,


            on_message=self.on_message,


            on_close=self.on_close,


            on_error=self.on_error

        )



        self.ws.run_forever(

            ping_interval=20,

            ping_timeout=10

        )









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



        self.auth()



    # =====================================================
    # AUTH
    # =====================================================

    def auth(self):


        args = self.generate_signature()



        self.ws.send(

            json.dumps(

                {


                    "op":

                        "auth",


                    "args":

                        [

                            BYBIT_API_KEY,


                            args[1],


                            args[2]

                        ]

                }

            )

        )









    # =====================================================
    # SUBSCRIBE
    # =====================================================

    def subscribe(self):


        self.ws.send(

            json.dumps(

                {


                    "op":

                        "subscribe",


                    "args":

                        [

                            "position",

                            "order"

                        ]

                }

            )

        )



        print(

            "[PRIVATE WS SUBSCRIBED]"

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



            topic = data.get(

                "topic"

            )



            if data.get("op") == "auth":


                if data.get("success"):


                    print(

                        "[PRIVATE WS AUTH OK]"

                    )


                    self.subscribe()



                return







            if topic == "position":


                rows = (

                    data

                    .get("data",[])

                )



                for p in rows:


                    position_manager.update_from_ws(

                        p

                    )






            elif topic == "order":


                print(

                    "[ORDER UPDATE]",

                    data

                )






        except Exception as e:


            print(

                "[PRIVATE WS MESSAGE ERROR]",

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

private_ws = PrivateWS()
