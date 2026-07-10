# =====================================================
# services/private_ws.py
# Bybit Private WebSocket V5
# =====================================================

import json
import time
import threading
import websocket
import hmac
import hashlib



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


        self.subscribed = False



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

    def auth_message(self):


        expires = int(

            time.time()*1000

        ) + 10000




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
    # RUN LOOP
    # =====================================================

    def run(self):


        while self.running:


            try:


                self.authenticated = False


                self.subscribed = False



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





            self.connected = False



            if self.running:


                print(

                    "[PRIVATE WS RECONNECT]"

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



            op = data.get(

                "op"

            )



            # -----------------------------
            # AUTH RESPONSE
            # -----------------------------

            if op == "auth":



                if data.get(

                    "success"

                ):


                    self.authenticated = True



                    print(

                        "[PRIVATE WS AUTH OK]"

                    )



                    self.subscribe(ws)



                return







            # -----------------------------
            # SUBSCRIBE RESPONSE
            # -----------------------------

            if op == "subscribe":



                if data.get(

                    "success"

                ):


                    self.subscribed = True



                    print(

                        "[PRIVATE WS SUBSCRIBED]"

                    )



                return







            topic = data.get(

                "topic"

            )



            if topic == "execution":


                self.handle_execution(

                    data

                )



            elif topic == "position":


                self.handle_position(

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



        if self.subscribed:


            return



        ws.send(

            json.dumps(

                {


                    "op":

                    "subscribe",


                    "args":

                    [

                        "order",

                        "execution",

                        "position"

                    ]

                }

            )

        )









    # =====================================================
    # EXECUTION EVENT
    # =====================================================

    def handle_execution(
        self,
        data
    ):


        print(

            "[EXECUTION EVENT]"

        )


        position_manager.sync()







    # =====================================================
    # POSITION EVENT
    # =====================================================

    def handle_position(
        self,
        data
    ):


        print(

            "[POSITION EVENT]"

        )


        position_manager.sync()







    # =====================================================
    # ORDER EVENT
    # =====================================================

    def handle_order(
        self,
        data
    ):


        print(

            "[ORDER EVENT]"

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


        self.authenticated = False


        self.subscribed = False



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

            self.connected,


            "authenticated":

            self.authenticated,


            "subscribed":

            self.subscribed


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
