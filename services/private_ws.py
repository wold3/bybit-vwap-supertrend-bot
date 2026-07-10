# =====================================================
# services/private_ws.py
# Bybit V5 Private WebSocket
# =====================================================


import time
import json
import hmac
import hashlib
import threading
import websocket




from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET
)


from portfolio.position_manager import (
    position_manager
)


from web.server import (
    add_log
)





WS_URL = (

    "wss://stream.bybit.com/v5/private"

)






class PrivateWS:



    def __init__(self):


        self.ws = None


        self.running = False


        self.thread = None



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
    # MAIN LOOP
    # =====================================================

    def run(self):


        while self.running:


            try:



                print(

                    "[PRIVATE WS CONNECTING]"

                )



                self.ws = websocket.WebSocketApp(

                    WS_URL,


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







            if self.running:



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


            if data.get(

                "op"

            ) == "auth":



                if data.get(

                    "success"

                ):



                    print(

                        "[PRIVATE WS AUTH OK]"

                    )



                    self.subscribe()



                return







            topic = data.get(

                "topic"

            )







            # POSITION


            if topic == "position":



                items = data.get(

                    "data",

                    []

                )



                for p in items:



                    position_manager.update(

                        p

                    )



                return







            # ORDER


            if topic == "order":



                print(

                    "[ORDER UPDATE]",

                    data

                )



                add_log(

                    str(data)

                )



        except Exception as e:



            print(

                "[PRIVATE WS MESSAGE ERROR]",

                e

            )









    # =====================================================
    # SUBSCRIBE
    # =====================================================

    def subscribe(self):


        msg = {


            "op":

                "subscribe",


            "args":

                [

                    "position",

                    "order"

                ]

        }





        self.ws.send(

            json.dumps(msg)

        )



        print(

            "[PRIVATE WS SUBSCRIBED]"

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
# SINGLETON
# =====================================================

private_ws = PrivateWS()
