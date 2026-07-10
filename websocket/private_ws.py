import json
import threading
import time

from pybit.unified_trading import WebSocket

from config import (
    BYBIT_TESTNET,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    CATEGORY,
)


# ==========================================
# BYBIT PRIVATE WEBSOCKET V5
# ==========================================

class PrivateWS:


    def __init__(self):

        self.ws = None

        self.running = False

        self.position = None
        self.orders = None
        self.wallet = None


        print("==============================")
        print("[PRIVATE WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("==============================")



    # ======================================
    # CALLBACK
    # ======================================

    def handle_message(self, message):

        try:

            topic = message.get("topic")


            if topic == "position":

                self.position = message

                print("[POSITION UPDATE]")
                print(message)



            elif topic == "order":

                self.orders = message

                print("[ORDER UPDATE]")
                print(message)



            elif topic == "wallet":

                self.wallet = message

                print("[WALLET UPDATE]")
                print(message)



        except Exception as e:

            print(
                "[PRIVATE WS ERROR]",
                e
            )



    # ======================================
    # START
    # ======================================

    def start(self):


        if self.running:

            return



        self.running = True



        self.ws = WebSocket(

            testnet=BYBIT_TESTNET,

            channel_type="private",

            api_key=BYBIT_API_KEY,

            api_secret=BYBIT_API_SECRET

        )


        self.ws.position_stream(

            callback=self.handle_message

        )


        self.ws.order_stream(

            callback=self.handle_message

        )


        self.ws.wallet_stream(

            callback=self.handle_message

        )



        print("[PRIVATE WS STARTED]")



        while self.running:

            time.sleep(1)



    # ======================================
    # THREAD START
    # ======================================

    def run_thread(self):


        thread = threading.Thread(

            target=self.start,

            daemon=True

        )


        thread.start()



    # ======================================
    # STOP
    # ======================================

    def stop(self):


        self.running = False


        print("[PRIVATE WS STOPPED]")



    # ======================================
    # GETTERS
    # ======================================

    def get_position(self):

        return self.position



    def get_orders(self):

        return self.orders



    def get_wallet(self):

        return self.wallet





# ==========================================
# SINGLETON
# ==========================================

private_ws = PrivateWS()
