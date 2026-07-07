import os
import json
import time
import hmac
import hashlib
import websocket


class BybitPrivateWS:


    def __init__(self):

        self.api_key = os.getenv(
            "BYBIT_API_KEY"
        )

        self.api_secret = os.getenv(
            "BYBIT_API_SECRET"
        )

        self.url = (
            "wss://stream.bybit.com/v5/private"
        )



    # ======================================
    # AUTH
    # ======================================

    def auth(self, ws):

        expires = int(
            (time.time() + 10) * 1000
        )


        sign = hmac.new(

            self.api_secret.encode(),

            f"GET/realtime{expires}".encode(),

            hashlib.sha256

        ).hexdigest()



        ws.send(json.dumps({

            "op": "auth",

            "args": [

                self.api_key,

                expires,

                sign

            ]

        }))



    # ======================================
    # OPEN
    # ======================================

    def on_open(self, ws):

        print(
            "🔐 BYBIT PRIVATE WS CONNECTED"
        )


        self.auth(ws)



        ws.send(json.dumps({

            "op":"subscribe",

            "args":[

                "execution",

                "position",

                "wallet"

            ]

        }))





    # ======================================
    # MESSAGE
    # ======================================

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



            # ==============================
            # REAL FILL
            # ==============================

            if topic == "execution":

                self.handle_fill(
                    data
                )



            # ==============================
            # POSITION UPDATE
            # ==============================

            elif topic == "position":


                self.handle_position(
                    data
                )



            # ==============================
            # WALLET UPDATE
            # ==============================

            elif topic == "wallet":

                self.handle_wallet(
                    data
                )



        except Exception as e:


            print(
                "[PRIVATE WS MESSAGE ERROR]",
                e
            )




    # ======================================
    # FILL HANDLER
    # ======================================

    def handle_fill(
        self,
        data
    ):


        from execution.execution_engine import execution_engine



        fills = data.get(
            "data",
            []
        )



        for fill in fills:


            execution_engine.on_fill(

                symbol=fill.get(
                    "symbol"
                ),

                side=fill.get(
                    "side"
                ),

                qty=float(

                    fill.get(
                        "execQty",
                        0
                    )

                ),

                price=float(

                    fill.get(
                        "execPrice",
                        0
                    )

                )

            )





    # ======================================
    # POSITION HANDLER
    # ======================================

    def handle_position(
        self,
        data
    ):


        from position.position_manager import position_manager



        position_manager.update_position(

            data.get(
                "data",
                []
            )

        )


        print(
            "📌 POSITION UPDATED"
        )





    # ======================================
    # WALLET HANDLER
    # ======================================

    def handle_wallet(
        self,
        data
    ):


        print(
            "💰 WALLET UPDATE",
            data
        )





    # ======================================
    # START
    # ======================================

    def start(self):


        ws = websocket.WebSocketApp(

            self.url,

            on_open=self.on_open,

            on_message=self.on_message

        )



        ws.run_forever()



private_ws = BybitPrivateWS()
