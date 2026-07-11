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

    def get_auth(self):


        expires = int(

            time.time()*1000

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





                self.ws.run_forever()





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


        print(

            "[PRIVATE WS CONNECTED]"

        )


        add_log(

            "PRIVATE WS CONNECTED"

        )





        ws.send(

            json.dumps(

                self.get_auth()

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



            if data.get(

                "success"

            ):


                print(

                    "[WS AUTH OK]"

                )



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

                        rows[0]

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



        if self.ws:


            self.ws.close()



        print(

            "[PRIVATE WS STOPPED]"

        )









# =====================================================
# INSTANCE
# =====================================================

private_ws = PrivateWebSocket()
