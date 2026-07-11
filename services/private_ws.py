# =====================================================
# services/private_ws.py
# VWAP SUPERTREND BOT
# Bybit V5 Private WebSocket Manager
# =====================================================

import json
import time
import threading
import hmac
import hashlib

import websocket


from config import (

    DEMO_API_KEY,
    DEMO_API_SECRET,

    LIVE_API_KEY,
    LIVE_API_SECRET

)


from web.server import (

    add_log,
    get_trading_mode,
    update_status

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

        self.last_message = time.time()

        self.lock = threading.Lock()

        self.current_mode = None


        print(
            "[PRIVATE WS READY]"
        )





    # =====================================================
    # URL
    # =====================================================

    def get_url(self):


        if get_trading_mode() == "DEMO":

            return "wss://stream-demo.bybit.com/v5/private"


        return "wss://stream.bybit.com/v5/private"







    # =====================================================
    # API
    # =====================================================

    def api_key(self):

        if get_trading_mode() == "DEMO":

            return DEMO_API_KEY


        return LIVE_API_KEY






    def api_secret(self):

        if get_trading_mode() == "DEMO":

            return DEMO_API_SECRET


        return LIVE_API_SECRET







    # =====================================================
    # AUTH
    # =====================================================

    def auth_message(self):


        expires = (

            int(time.time()*1000)

            +

            10000

        )


        payload = (

            "GET/realtime"

            +

            str(expires)

        )


        signature = hmac.new(

            self.api_secret().encode(),

            payload.encode(),

            hashlib.sha256

        ).hexdigest()



        return {

            "op":"auth",

            "args":[

                self.api_key(),

                expires,

                signature

            ]

        }







    # =====================================================
    # SUBSCRIBE
    # =====================================================

    def subscribe(self):


        if not self.ws:

            return



        topics = [

            "position",

            "execution",

            "wallet"

        ]



        self.ws.send(

            json.dumps({

                "op":"subscribe",

                "args":topics

            })

        )



        add_log(

            "PRIVATE WS SUBSCRIBE OK"

        )







    # =====================================================
    # OPEN
    # =====================================================

    def on_open(self, ws):


        add_log(

            "PRIVATE WS CONNECTED"

        )


        self.authenticated=False



        ws.send(

            json.dumps(

                self.auth_message()

            )

        )







    # =====================================================
    # MESSAGE
    # =====================================================

    def on_message(self, ws, message):


        try:


            self.last_message=time.time()


            data=json.loads(message)



            # ---------------------
            # AUTH
            # ---------------------

            if data.get("op")=="auth":


                if data.get("success"):


                    self.authenticated=True


                    add_log(

                        "PRIVATE WS AUTH OK"

                    )


                    self.subscribe()



                else:


                    add_log(

                        "PRIVATE WS AUTH FAILED"

                    )


                return






            # ---------------------
            # SUBSCRIBE
            # ---------------------

            if data.get("op")=="subscribe":

                return





            topic=data.get(

                "topic",

                ""

            )



            # ---------------------
            # POSITION
            # ---------------------

            if topic.startswith("position"):


                rows=data.get(

                    "data",

                    []

                )


                for row in rows:


                    try:


                        position_manager.update(

                            row

                        )


                    except Exception as e:


                        add_log(

                            f"POSITION UPDATE ERROR {e}"

                        )



                return





            # ---------------------
            # EXECUTION
            # ---------------------

            if topic.startswith("execution"):


                for item in data.get("data",[]):


                    add_log(

                        "EXECUTION "

                        +

                        str(item.get("side"))

                        +

                        " "

                        +

                        str(item.get("execQty"))

                        +

                        "@"

                        +

                        str(item.get("execPrice"))

                    )


                return






            # ---------------------
            # WALLET
            # ---------------------

            if topic.startswith("wallet"):


                add_log(

                    "WALLET UPDATE"

                )


                return





        except Exception as e:


            add_log(

                f"WS MESSAGE ERROR {e}"

            )







    # =====================================================
    # ERROR
    # =====================================================

    def on_error(self, ws, error):


        add_log(

            f"PRIVATE WS ERROR {error}"

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


        self.authenticated=False


        add_log(

            "PRIVATE WS CLOSED"

        )



        try:


            position_manager.refresh()


        except Exception:


            pass







    # =====================================================
    # LOOP
    # =====================================================

    def run(self):


        while self.running:


            try:


                mode=get_trading_mode()


                self.current_mode=mode



                url=self.get_url()



                add_log(

                    f"PRIVATE WS CONNECT {mode}"

                )



                self.ws=websocket.WebSocketApp(

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



            self.running=True



        self.thread=threading.Thread(

            target=self.run,

            daemon=True,

            name="PrivateWS"

        )


        self.thread.start()



        add_log(

            "PRIVATE WS START"

        )









    # =====================================================
    # STOP
    =====================================================

    def stop(self):


        with self.lock:


            self.running=False



        try:


            if self.ws:


                self.ws.close()



        except Exception:


            pass




        if self.thread:


            self.thread.join(

                timeout=3

            )



        self.ws=None

        self.thread=None

        self.authenticated=False



        add_log(

            "PRIVATE WS STOPPED"

        )









    # =====================================================
    # RESTART
    =====================================================

    def restart(self):


        add_log(

            "PRIVATE WS RESTART"

        )


        self.stop()


        time.sleep(1)


        self.start()








    # =====================================================
    # MODE CHANGE
    # =====================================================

    def change_mode(self):


        add_log(

            "PRIVATE WS MODE CHANGE"

        )


        self.restart()







# =====================================================
# INSTANCE
# =====================================================

private_ws = PrivateWS()
