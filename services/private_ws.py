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


        sign_payload = (
            f"GET/realtime{expires}"
        )


        signature = hmac.new(
            self.api_secret.encode(),
            sign_payload.encode(),
            hashlib.sha256
        ).hexdigest()


        ws.send(json.dumps({

            "op": "auth",

            "args": [
                self.api_key,
                expires,
                signature
            ]

        }))


    # ======================================
    # OPEN
    # ======================================

    def on_open(self, ws):

        print(
            "🔐 PRIVATE WS CONNECTED"
        )


        self.auth(ws)


        # 체결
        ws.send(json.dumps({

            "op":"subscribe",

            "args":[
                "execution"
            ]

        }))


        # 포지션
        ws.send(json.dumps({

            "op":"subscribe",

            "args":[
                "position"
            ]

        }))


        # Wallet
        ws.send(json.dumps({

            "op":"subscribe",

            "args":[
                "wallet"
            ]

        }))



    # ======================================
    # MESSAGE
    # ======================================

    def on_message(self, ws, message):

        data = json.loads(message)


        topic = data.get(
            "topic"
        )


        if topic == "execution":

            self.handle_fill(data)



        elif topic == "position":

            print(
                "POSITION UPDATE",
                data
            )



        elif topic == "wallet":

            print(
                "WALLET UPDATE",
                data
            )



    # ======================================
    # FILL PROCESS
    # ======================================

    def handle_fill(self, data):

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
