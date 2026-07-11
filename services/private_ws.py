# =====================================================
# services/private_ws.py
# Bybit V5 Private WebSocket
# =====================================================

import websocket
import json
import time
import threading
import hmac
import hashlib


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    LIVE
)


from portfolio.position_manager import (
    position_manager
)


from database.database import (
    database
)


from web.server import (
    add_log
)





class PrivateWS:


    def __init__(self):


        self.ws = None

        self.running = False

        self.thread = None


        if LIVE:

            self.url = (
                "wss://stream.bybit.com/v5/private"
            )

        else:

            self.url = (
                "wss://stream-demo.bybit.com/v5/private"
            )



        print(

            "[PRIVATE WS READY]"

        )









    # =====================================================
    # AUTH
    # =====================================================


    def auth_message(self):


        expires = (

            int(time.time()*1000)

            +

            10000

        )



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

                    self.url,


                    on_open=self.on_open,


                    on_message=self.on_message,


                    on_error=self.on_error,


                    on_close=self.on_close

                )



                self.ws.run_forever()



            except Exception as e:


                print(

                    "[WS ERROR]",

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



            # AUTH

            if data.get("op") == "auth":


                if data.get("success"):


                    print(

                        "[PRIVATE WS AUTH OK]"

                    )


                    self.subscribe()



                return







            topic = data.get(

                "topic"

            )




            if topic == "position":


                self.position_update(

                    data

                )





            elif topic == "execution":


                print(

                    "[EXECUTION]",

                    data

                )


                add_log(

                    "EXECUTION UPDATE"

                )





            elif topic == "order":


                print(

                    "[ORDER UPDATE]",

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


    def subscribe(self):


        args = [


            "position",


            "execution",


            "order"


        ]



        self.ws.send(

            json.dumps({

                "op":

                    "subscribe",


                "args":

                    args

            })

        )



        print(

            "[PRIVATE WS SUBSCRIBED]"

        )









    # =====================================================
    # POSITION UPDATE
    # =====================================================


    def position_update(
        self,
        data
    ):


        try:


            rows = (

                data

                .get(

                    "data",

                    []

                )

            )


            if rows:


                position_manager.update_from_ws(

                    rows[0]

                )



        except Exception as e:


            print(

                "[POSITION WS ERROR]",

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
