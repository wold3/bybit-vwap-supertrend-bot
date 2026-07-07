import os
import json
import time
import hmac
import hashlib
import websocket
from dotenv import load_dotenv


load_dotenv()



class BybitPrivateWS:


    def __init__(self):

        self.api_key = os.getenv(
            "BYBIT_API_KEY"
        )

        self.api_secret = os.getenv(
            "BYBIT_API_SECRET"
        )


        self.url = os.getenv(

            "PRIVATE_WS_URL",

            "wss://stream.bybit.com/v5/private"

        )



    # =====================================
    # AUTH
    # =====================================

    def auth(
        self,
        ws
    ):


        expires = int(

            (time.time() + 10)

            *

            1000

        )


        payload = (

            "GET/realtime"

            +

            str(expires)

        )



        signature = hmac.new(

            self.api_secret.encode(),

            payload.encode(),

            hashlib.sha256

        ).hexdigest()



        ws.send(json.dumps({

            "op":

                "auth",


            "args":

                [

                    self.api_key,

                    expires,

                    signature

                ]

        }))



    # =====================================
    # OPEN
    # =====================================

    def on_open(
        self,
        ws
    ):


        print(
            "🔐 PRIVATE WS CONNECTED"
        )



        self.auth(ws)



        time.sleep(1)



        ws.send(json.dumps({

            "op":

                "subscribe",


            "args":

                [

                    "execution",

                    "position",

                    "wallet"

                ]

        }))



        print(
            "PRIVATE CHANNEL SUBSCRIBED"
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



            # ==========================
            # 체결
            # ==========================

            if topic == "execution":


                self.handle_execution(

                    data

                )



            # ==========================
            # 포지션
            # ==========================

            elif topic == "position":


                self.handle_position(

                    data

                )



            # ==========================
            # 지갑
            # ==========================

            elif topic == "wallet":


                self.handle_wallet(

                    data

                )



        except Exception as e:


            print(

                "PRIVATE WS ERROR",

                e

            )





    # =====================================
    # EXECUTION FILL
    # =====================================

    def handle_execution(
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

                symbol=

                fill.get(
                    "symbol"
                ),


                side=

                fill.get(
                    "side"
                ),


                qty=

                float(

                    fill.get(
                        "execQty",
                        0
                    )

                ),


                price=

                float(

                    fill.get(
                        "execPrice",
                        0
                    )

                )

            )





    # =====================================
    # POSITION UPDATE
    # =====================================

    def handle_position(
        self,
        data
    ):


        from position.position_manager import position_manager

        from execution.execution_engine import execution_engine



        positions = data.get(
            "data",
            []
        )



        # Position 저장

        position_manager.update_position(

            positions

        )



        # Trailing Stop

        for p in positions:


            symbol = p.get(
                "symbol"
            )


            side = p.get(
                "side"
            )


            mark_price = p.get(
                "markPrice"
            )



            if not all(

                [

                    symbol,

                    side,

                    mark_price

                ]

            ):

                continue



            execution_engine.update_trailing_stop(

                symbol,

                side,

                float(mark_price)

            )



        print(
            "📌 POSITION UPDATED"
        )





    # =====================================
    # WALLET
    # =====================================

    def handle_wallet(
        self,
        data
    ):


        wallet = data.get(
            "data"
        )


        print(

            "💰 WALLET UPDATE",

            wallet

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

            "PRIVATE WS ERROR",

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

            "PRIVATE WS CLOSED",

            code,

            msg

        )





    # =====================================
    # START
    # =====================================

    def start(self):


        while True:


            try:


                ws = websocket.WebSocketApp(

                    self.url,

                    on_open=self.on_open,

                    on_message=self.on_message,

                    on_error=self.on_error,

                    on_close=self.on_close

                )


                ws.run_forever()



            except Exception as e:


                print(

                    "PRIVATE WS RECONNECT",

                    e

                )



            time.sleep(5)





private_ws = BybitPrivateWS()
