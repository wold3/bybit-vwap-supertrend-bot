# services/private_ws.py


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




        print(
            "[PRIVATE WS READY]"
        )





    # =====================================
    # START
    # =====================================

    def start(self):


        if self.running:

            return



        self.running = True



        self.thread = threading.Thread(

            target=self.run

        )


        self.thread.daemon = True


        self.thread.start()





    # =====================================
    # AUTH
    # =====================================

    def auth_message(self):


        expires = int(

            time.time() * 1000

        ) + 10000



        signature = hmac.new(

            BYBIT_API_SECRET.encode(),

            f"GET/realtime{expires}".encode(),

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






    # =====================================
    # RUN
    # =====================================

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



                self.ws.run_forever()



            except Exception as e:


                print(

                    "[PRIVATE WS ERROR]",

                    e

                )



            time.sleep(5)








    # =====================================
    # OPEN
    # =====================================

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



        time.sleep(1)



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







    # =====================================
    # MESSAGE
    # =====================================

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







    # =====================================
    # EXECUTION
    # =====================================

    def handle_execution(
        self,
        data
    ):


        print(

            "[EXECUTION EVENT]",

            data

        )



        position_manager.sync()








    # =====================================
    # POSITION
    # =====================================

    def handle_position(
        self,
        data
    ):


        print(

            "[POSITION EVENT]"

        )


        position_manager.sync()








    # =====================================
    # ORDER
    # =====================================

    def handle_order(
        self,
        data
    ):


        print(

            "[ORDER EVENT]",

            data

        )








    # =====================================
    # ERROR
    # =====================================

    def on_error(
        self,
        ws,
        error
    ):


        print(

            "[PRIVATE WS ERROR]",

            error

        )







    # =====================================
    # CLOSE
    # =====================================

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







    # =====================================
    # STOP
    # =====================================

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
