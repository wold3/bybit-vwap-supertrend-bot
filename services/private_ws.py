# services/private_ws.py

import os
import time
import json
import hmac
import hashlib
import threading

import websocket

from dotenv import load_dotenv


from position.position_manager import position_manager

from execution.execution_engine import execution_engine

from trade_db import trade_db

from watchdog.watchdog import watchdog



load_dotenv()





class PrivateWS:


    def __init__(self):


        self.api_key = os.getenv(

            "BYBIT_API_KEY",

            ""

        )


        self.api_secret = os.getenv(

            "BYBIT_API_SECRET",

            ""

        )


        self.url = os.getenv(

            "BYBIT_PRIVATE_WS",

            "wss://stream-testnet.bybit.com/v5/private"

        )



        self.running = False

        self.connected = False


        self.ws = None

        self.thread = None





    # =====================================
    # START
    # =====================================

    def start(self):


        if self.running:

            return



        self.running = True



        self.thread = threading.Thread(

            target=self._run,

            daemon=True

        )


        self.thread.start()



        print(

            "[PRIVATE WS START]"

        )





    # =====================================
    # RUN
    # =====================================

    def _run(self):


        while self.running:


            try:


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

                    "[PRIVATE WS ERROR]",

                    e

                )



            time.sleep(5)





    # =====================================
    # AUTH SIGN
    # =====================================

    def generate_auth(self):


        expires = int(

            time.time() * 1000

        ) + 10000



        param = (

            "GET/realtime"

            +

            str(expires)

        )



        signature = hmac.new(

            self.api_secret.encode(),

            param.encode(),

            hashlib.sha256

        ).hexdigest()



        return {


            "op":

                "auth",


            "args":

                [

                    self.api_key,

                    expires,

                    signature

                ]

        }





    # =====================================
    # OPEN
    # =====================================

    def on_open(
        self,
        ws
    ):


        self.connected = True



        ws.send(

            json.dumps(

                self.generate_auth()

            )

        )



        time.sleep(1)



        subscribe = {


            "op":

                "subscribe",


            "args":

                [

                    "execution",

                    "position",

                    "wallet"

                ]

        }



        ws.send(

            json.dumps(

                subscribe

            )

        )



        print(

            "[PRIVATE AUTH OK]"

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


            watchdog.heartbeat(

                "private_ws"

            )



            topic = data.get(

                "topic"

            )



            if topic == "execution":


                self.handle_execution(

                    data.get("data")

                )



            elif topic == "position":


                self.handle_position(

                    data.get("data")

                )



        except Exception as e:


            print(

                "[PRIVATE MESSAGE ERROR]",

                e

            )





    # =====================================
    # EXECUTION EVENT
    # =====================================

    def handle_execution(
        self,
        data
    ):


        if not data:

            return



        for item in data:


            symbol = item.get(

                "symbol"

            )


            side = item.get(

                "side"

            )


            qty = float(

                item.get(

                    "execQty",

                    0

                )

            )


            price = float(

                item.get(

                    "execPrice",

                    0

                )

            )



            print(

                "[FILL]",

                symbol,

                side,

                qty,

                price

            )



            execution_engine.on_fill(

                symbol,

                side,

                qty,

                price

            )





    # =====================================
    # POSITION EVENT
    # =====================================

    def handle_position(
        self,
        data
    ):


        if not data:

            return



        for item in data:


            symbol = item.get(

                "symbol"

            )


            size = float(

                item.get(

                    "size",

                    0

                )

            )


            side = item.get(

                "side"

            )



            if size > 0:


                position_manager.set_position(

                    symbol,

                    side,

                    size,

                    float(

                        item.get(

                            "avgPrice",

                            0

                        )

                    )

                )



            else:


                position_manager.remove_position(

                    symbol

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

            "[PRIVATE ERROR]",

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


        self.connected = False


        print(

            "[PRIVATE CLOSED]"

        )





    # =====================================
    # STOP
    # =====================================

    def stop(self):


        self.running = False


        self.connected = False



        if self.ws:

            self.ws.close()





    # =====================================
    # STATUS
    # =====================================

    def status(self):


        return {


            "running":

                self.running,


            "connected":

                self.connected

        }





private_ws = PrivateWS()
