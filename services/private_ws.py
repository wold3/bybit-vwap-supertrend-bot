# =====================================================
# services/private_ws.py
# =====================================================

import json
import time
import threading
import hmac
import hashlib
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

        self.thread = None

        self.connected = False

        self.authenticated = False


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

            target=self.run

        )


        self.thread.daemon = True


        self.thread.start()



    # =====================================================
    # AUTH
    # =====================================================

    def auth_message(self):


        expires = int(

            time.time() * 1000

        ) + 10000



        payload = (

            "GET/realtime"

            +

            str(expires)

        )



        signature = hmac.new(

            BYBIT_API_SECRET.encode(),

            payload.encode(),

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


                print(

                    "[PRIVATE WS CONNECTING]"

                )


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

                    "[PRIVATE WS RUN ERROR]",

                    e

                )



            self.connected = False

            self.authenticated = False



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


        self.connected = True



        ws.send(

            json.dumps(

                self.auth_message()

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



            if data.get("op") == "auth":


                if data.get("success"):


                    self.authenticated = True


                    print(

                        "[PRIVATE WS AUTH OK]"

                    )



                    self.subscribe(ws)


                else:


                    print(

                        "[PRIVATE WS AUTH FAIL]",

                        data

                    )



                return





            topic = data.get(

                "topic"

            )



            if topic == "position":


                self.handle_position(

                    data

                )



            elif topic == "execution":


                self.handle_execution(

                    data

                )



            elif topic == "order":


                self.handle_order(

                    data

                )



        except Exception as e:


            print(

                "[WS MESSAGE ERROR]",

                e

            )





    # =====================================================
    # SUBSCRIBE
    # =====================================================

    def subscribe(
        self,
        ws
    ):


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





    # =====================================================
    # POSITION
    # =====================================================

    def handle_position(
        self,
        data
    ):


        print(

            "[POSITION UPDATE]"

        )


        position_manager.sync()





    # =====================================================
    # EXECUTION
    # =====================================================

    def handle_execution(
        self,
        data
    ):


        print(

            "[EXECUTION UPDATE]"

        )


        position_manager.sync()





    # =====================================================
    # ORDER
    # =====================================================

    def handle_order(
        self,
        data
    ):


        print(

            "[ORDER UPDATE]"

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


        self.connected = False

        self.authenticated = False





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





private_ws = PrivateWebSocket()
