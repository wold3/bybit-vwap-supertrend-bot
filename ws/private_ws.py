import threading
import time

from pybit.unified_trading import WebSocket

from config import (
    BYBIT_TESTNET,
    BYBIT_DEMO,
    BYBIT_API_KEY,
    BYBIT_API_SECRET,
    CATEGORY,
)


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
    # CALLBACK
    # ======================================

    def handle_position(self, message):

        try:

            self.position = message

            print("[POSITION UPDATE]")
            print(message)


        except Exception as e:

            print(
                "[POSITION CALLBACK ERROR]",
                e
            )


    def handle_order(self, message):

        try:

            self.orders = message

            print("[ORDER UPDATE]")
            print(message)


        except Exception as e:

            print(
                "[ORDER CALLBACK ERROR]",
                e
            )


    def handle_wallet(self, message):

        try:

            self.wallet = message

            print("[PRIVATE WALLET UPDATE]")


        except Exception as e:

            print(
                "[WALLET CALLBACK ERROR]",
                e
            )



    # ======================================
    # START
    # ======================================

    def start(self):

        if self.running:

            return


        try:

            self.running = True


            self.ws = WebSocket(

                testnet=BYBIT_TESTNET,

                demo=BYBIT_DEMO,

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


        self.running = False


        try:

            if self.ws:

                self.ws.exit()


        except:

            pass



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





private_ws = PrivateWS()
