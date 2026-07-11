# =====================================================
# services/private_ws.py
# Bybit V5 Private WebSocket
# =====================================================

import json
import time
import hmac
import hashlib
import threading


import websocket



from config import (
    BYBIT_API_KEY,
    BYBIT_API_SECRET
)


from web.server import (
    get_trading_mode,
    add_log
)


from portfolio.position_manager import (
    position_manager
)








class PrivateWebSocket:


    def __init__(self):


        self.ws = None


        self.running = False


        self.thread = None



        self.authenticated = False


        self.subscribed = False



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


        return (
            "wss://stream.bybit.com/v5/private"
        )









    # =====================================================
    # AUTH
    # =====================================================

    def create_auth(self):


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
    # START
    # =====================================================

    def start(self):


        if self.running:


            return



        self.running = True



        self.thread = threading.Thread(

            target=self.loop,

            daemon=True

        )


        self.thread.start()










    # =====================================================
    # LOOP
    # =====================================================

    def loop(self):


        while self.running:


            try:


                self.authenticated = False

                self.subscribed = False



                url = self.get_url()



                print(

                    "[PRIVATE WS CONNECT]",

                    url

                )





                self.ws = websocket.WebSocketApp(


                    url,


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

                    "[PRIVATE WS LOOP ERROR]",

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


        add_log(

            "PRIVATE WS CONNECTED"

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





            # -------------------------
            # AUTH RESPONSE
            # -------------------------

            if (

                data.get("op")

                ==

                "auth"

            ):


                if data.get(

                    "success"

                ):


                    self.authenticated = True



                    print(

                        "[WS AUTH OK]"

                    )



                    self.subscribe(ws)



                return







            # -------------------------
            # SUBSCRIBE RESPONSE
            # -------------------------

            if (

                data.get("op")

                ==

                "subscribe"

            ):


                if data.get(

                    "success"

                ):


                    self.subscribed = True



                    print(

                        "[WS SUBSCRIBE OK]"

                    )



                return







            topic = data.get(

                "topic"

            )







            # -------------------------
            # POSITION
            # -------------------------

            if topic == "position":


                rows = data.get(

                    "data",

                    []

                )



                if rows:


                    position_manager.update_from_ws(

                        rows

                    )









            # -------------------------
            # ORDER
            # -------------------------

            elif topic == "order":


                add_log(

                    "ORDER UPDATE"

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

        self.subscribed = False



        print(

            "[PRIVATE WS CLOSED]"

        )


        add_log(

            "PRIVATE WS CLOSED"

        )









    # =====================================================
    # STOP
    # =====================================================

    def stop(self):


        self.running = False



        self.authenticated = False

        self.subscribed = False



        if self.ws:


            self.ws.close()



        print(

            "[PRIVATE WS STOPPED]"

        )









# =====================================================
# INSTANCE
# =====================================================

private_ws = PrivateWebSocket()
