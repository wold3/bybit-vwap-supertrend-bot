import os
import json
import time
import threading
import websocket

from dotenv import load_dotenv

from watchdog.watchdog import watchdog


load_dotenv()



class PrivateWSClient:


    def __init__(self):


        live = os.getenv(
            "LIVE_TRADING",
            "false"
        ).lower() == "true"



        if live:

            self.url = os.getenv(
                "BYBIT_LIVE_PRIVATE_WS",
                "wss://stream.bybit.com/v5/private"
            )

        else:

            self.url = os.getenv(
                "BYBIT_DEMO_PRIVATE_WS",
                "wss://stream-demo.bybit.com/v5/private"
            )



        self.api_key = os.getenv(
            "BYBIT_API_KEY"
        )

        self.api_secret = os.getenv(
            "BYBIT_API_SECRET"
        )


        self.running = False

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
    # CONNECT LOOP
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


                self.ws.run_forever(

                    ping_interval=20,

                    ping_timeout=10

                )


            except Exception as e:


                print(
                    "[PRIVATE LOOP ERROR]",
                    e
                )


            time.sleep(5)





    # =====================================
    # AUTH
    # =====================================

    def on_open(
        self,
        ws
    ):


        print(
            "[PRIVATE CONNECTED]"
        )


        if not self.api_key or not self.api_secret:

            print(
                "[PRIVATE AUTH SKIP]"
            )

            return



        expires = int(
            time.time()*1000
        ) + 10000



        import hmac
        import hashlib



        sign = hmac.new(

            self.api_secret.encode(),

            f"GET/realtime{expires}".encode(),

            hashlib.sha256

        ).hexdigest()



        payload = {

            "op":
                "auth",

            "args":
                [

                    self.api_key,

                    expires,

                    sign

                ]

        }



        ws.send(

            json.dumps(payload)

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


            watchdog.heartbeat()



            if data.get("op") == "auth":


                if data.get("success"):

                    print(
                        "[PRIVATE AUTH SUCCESS]"
                    )


                return



            topic = data.get(
                "topic"
            )


            if topic:


                print(
                    "[PRIVATE EVENT]",
                    topic
                )



        except Exception as e:


            print(
                "[PRIVATE MESSAGE ERROR]",
                e
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
            "[PRIVATE WS ERROR]",
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
            "[PRIVATE WS CLOSED]"
        )





    # =====================================
    # STOP
    # =====================================

    def stop(self):


        self.running = False


        if self.ws:


            try:

                self.ws.close()

            except:

                pass


        print(
            "[PRIVATE WS STOPPED]"
        )





private_ws_client = PrivateWSClient()
