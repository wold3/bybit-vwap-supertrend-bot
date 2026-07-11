# =====================================================
# services/private_ws.py
# Bybit Private WebSocket Manager
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
    CATEGORY,
    DEFAULT_SYMBOL
)


from portfolio.position_manager import (
    position_manager
)


from web.server import (
    update_status,
    add_log
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
    # START
    # =====================================================


    def start(self):


        if self.running:

            return



        self.running = True



        self.thread = threading.Thread(

            target=self.connect_loop,

            daemon=True

        )


        self.thread.start()







    # =====================================================
    # CONNECT LOOP
    # =====================================================


    def connect_loop(self):


        while self.running:


            try:


                print(

                    "[PRIVATE WS CONNECTING]"

                )


                self.ws = websocket.WebSocketApp(

                    "wss://stream.bybit.com/v5/private",


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
    # AUTH
    # =====================================================


    def auth(self):


        expires = int(

            (time.time()+1)

            *

            1000

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



        message = {


            "op":

                "auth",


            "args":

                [

                    BYBIT_API_KEY,

                    expires,

                    signature

                ]

        }



        self.ws.send(

            json.dumps(message)

        )









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



        self.auth()



        time.sleep(1)



        ws.send(

            json.dumps({

                "op":

                    "subscribe",


                "args":

                    [

                        "position",

                        "order"

                    ]

            })

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

                "topic",

                ""

            )





            if topic == "position":


                self.position_update(

                    data

                )





            elif topic == "order":


                self.order_update(

                    data

                )






        except Exception as e:


            print(

                "[WS MESSAGE ERROR]",

                e

            )









    # =====================================================
    # POSITION UPDATE
    # =====================================================


    def position_update(
        self,
        data
    ):


        try:


            item = data["data"][0]



            position_manager.update_from_ws(

                item

            )



            add_log(

                "[POSITION WS UPDATE]"

            )



        except Exception as e:


            print(

                "[POSITION UPDATE ERROR]",

                e

            )









    # =====================================================
    # ORDER UPDATE
    # =====================================================


    def order_update(
        self,
        data
    ):


        try:


            order = data["data"][0]



            status = order.get(

                "orderStatus",

                ""

            )



            update_status({

                "order":

                    status

            })



            print(

                "[ORDER WS]",

                status

            )



        except Exception as e:


            print(

                "[ORDER UPDATE ERROR]",

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
