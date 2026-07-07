import os
import time
import json
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


    # =====================================
    # AUTH
    # =====================================

    def auth(self, ws):

        expires = int(
            (time.time() + 10) * 1000
        )


        signature = hmac.new(
            self.api_secret.encode(),
            f"GET/realtime{expires}".encode(),
            hashlib.sha256
        ).hexdigest()


        msg = {
            "op": "auth",
            "args": [
                self.api_key,
                expires,
                signature
            ]
        }


        ws.send(
            json.dumps(msg)
        )



    # =====================================
    # OPEN
    # =====================================

    def on_open(self, ws):

        print(
            "🔐 BYBIT PRIVATE WS CONNECTED"
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


        # 잔고
        ws.send(json.dumps({
            "op":"subscribe",
            "args":[
                "wallet"
            ]
        }))



    # =====================================
    # MESSAGE
    # =====================================

    def on_message(self, ws, message):

        data = json.loads(message)


        topic = data.get(
            "topic"
        )


        # -----------------------------
        # 체결
        # -----------------------------

        if topic == "execution":

            print(
                "✅ FILL:",
                data
            )


            self.handle_fill(
                data
            )



        # -----------------------------
        # 포지션
        # -----------------------------

        elif topic == "position":

            print(
                "📌 POSITION:",
                data
            )


        # -----------------------------
        # 지갑
        # -----------------------------

        elif topic == "wallet":

            print(
                "💰 WALLET:",
                data
            )



    def handle_fill(self, data):

        # execution_engine 연결 자리

        pass



    # =====================================
    # START
    # =====================================

    def start(self):

        ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message
        )


        ws.run_forever()



private_ws = BybitPrivateWS()
