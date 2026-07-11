# =====================================================
# services/private_ws.py
# Bybit V5 Private WebSocket Manager
# =====================================================

import json
import time
import threading
import websocket
import hmac
import hashlib


from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET
)


from web.server import (
    add_log,
    get_trading_mode
)


from portfolio.position_manager import (
    position_manager
)





class PrivateWS:


    def __init__(self):

        self.ws = None

        self.thread = None

        self.running = False

        self.authenticated = False

        self.lock = threading.Lock()

        print(
            "[PRIVATE WS READY]"
        )









    # =====================================================
    # URL
    # =====================================================

    def get_url(self):


        mode = get_trading_mode()



        if mode == "DEMO":


            return (

                "wss://stream-demo.bybit.com/v5/private"

            )


        else:


            return (

                "wss://stream.bybit.com/v5/private"

            )











    # =====================================================
    # AUTH
    # =====================================================

    def auth_message(self):


        expires = (

            int(time.time() * 1000)

            +

            10000

        )


        param = (

            "GET/realtime"

            +

            str(expires)

        )


        signature = hmac.new(

            bytes(

                BYBIT_API_SECRET,

                "utf-8"

            ),

            bytes(

                param,

                "utf-8"

            ),

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
    # SUBSCRIBE
    # =====================================================

    def subscribe(self):


        topics = [


            "position",


            "execution"


        ]



        self.ws.send(

            json.dumps({

                "op":

                    "subscribe",


                "args":

                    topics

            })

        )


        print(

            "[WS SUBSCRIBE OK]"

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





            if op == "auth":



                if data.get(

                    "success"

                ):



                    if not self.authenticated:


                        print(

                            "[WS AUTH OK]"

                        )



                    self.authenticated = True



                    self.subscribe()



                return









            topic = data.get(

                "topic"

            )





            if topic == "position":



                position_manager.update(

                    data.get(

                        "data"

                    )

                )





            elif topic == "execution":



                add_log(

                    "EXECUTION UPDATE"

                )






        except Exception as e:



            add_log(

                f"WS MESSAGE ERROR {e}"

            )









    # =====================================================
    # ERROR
    # =====================================================

    def on_error(

        self,

        ws,

        error

    ):


        add_log(

            f"WS ERROR {error}"

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


        self.authenticated = False



        print(

            "[PRIVATE WS CLOSED]"

        )









    # =====================================================
    # LOOP
    # =====================================================

    def run(self):


        while self.running:


            try:



                url = self.get_url()



                print(

                    "[PRIVATE WS CONNECT]",

                    url

                )





                self.authenticated = False



                self.ws = websocket.WebSocketApp(

                    url,

                    on_open=self.on_open,

                    on_message=self.on_message,

                    on_error=self.on_error,

                    on_close=self.on_close

                )



                self.ws.run_forever()



            except Exception as e:



                add_log(

                    f"WS LOOP ERROR {e}"

                )



            if self.running:


                time.sleep(5)









    # =====================================================
    # START
    # =====================================================

    def start(self):


        with self.lock:


            if self.running:


                return



            self.running = True





        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )


        self.thread.start()










    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        with self.lock:


            self.running = False



        try:



            if self.ws:


                self.ws.close()



        except:


            pass



        self.ws = None



        self.authenticated = False



        print(

            "[PRIVATE WS STOPPED]"

        )











# =====================================================
# INSTANCE
# =====================================================

private_ws = PrivateWS()
