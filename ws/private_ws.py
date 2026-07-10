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
# PRIVATE WEBSOCKET V5
# ==========================================

class PrivateWS:


    def __init__(self):

        self.ws = None

        self.running = False

        self.position = {}

        self.orders = {}

        self.wallet = {}

        print("==============================")
        print("[PRIVATE WS INIT]")
        print("CATEGORY :", CATEGORY)
        print("==============================")



    # ======================================
    # MESSAGE HANDLER
    # ======================================

    def handle_position(self, message):

        try:

            self.position = message

            print("[POSITION UPDATE]")

        except Exception as e:

            print(
                "[POSITION WS ERROR]",
                e
            )



    def handle_order(self, message):

        try:

            self.orders = message

            print("[ORDER UPDATE]")

        except Exception as e:

            print(
                "[ORDER WS ERROR]",
                e
            )



    def handle_wallet(self, message):

        try:

            self.wallet = message

            print("[WALLET UPDATE]")

        except Exception as e:

            print(
                "[WALLET WS ERROR]",
                e
            )



    # ======================================
    # START
    # ======================================

    def start(self):


        if self.running:

            return


        self.running = True


        try:


            self.ws = WebSocket(

                testnet=BYBIT_TESTNET,

                channel_type="private",

                api_key=BYBIT_API_KEY,

                api_secret=BYBIT_API_SECRET

            )



            self.ws.position_stream(

                callback=self.handle_position

            )


            self.ws.order_stream(

                callback=self.handle_order

            )


            self.ws.wallet_stream(

                callback=self.handle_wallet

            )


            print("[PRIVATE WS STARTED]")


            while self.running:

                time.sleep(1)



        except Exception as e:


            print(
                "[PRIVATE WS START ERROR]",
                e
            )


            self.running=False




    # ======================================
    # THREAD
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


        self.running=False


        print("[PRIVATE WS STOPPED]")



    # ======================================
    # DATA ACCESS
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
