import threading
import time


from watchdog.watchdog import watchdog

from position.position_manager import position_manager

from risk.drawdown_guard import drawdown_guard



class PrivateWS:
    """
    Bybit Private WebSocket

    담당:
    - execution event
    - position event
    - wallet event
    """



    def __init__(self):

        self.running = False

        self.connected = False

        self.thread = None





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
            "🔐 PRIVATE WS START"
        )





    def _run(self):

        self.connected = True


        print(
            "PRIVATE CHANNEL SUBSCRIBED"
        )


        while self.running:


            try:

                watchdog.heartbeat(
                    "private_ws"
                )


                # 실제 Bybit Private WS 위치


                time.sleep(1)



            except Exception as e:


                print(
                    "[PRIVATE WS ERROR]",
                    e
                )


                time.sleep(5)



        self.connected = False





    # =====================================
    # MESSAGE ROUTER
    # =====================================

    def handle_message(
        self,
        data
    ):


        topic = data.get(
            "topic"
        )


        if topic == "execution":

            self.handle_execution(
                data
            )


        elif topic == "position":

            self.handle_position(
                data
            )


        elif topic == "wallet":

            self.handle_wallet(
                data
            )





    # =====================================
    # EXECUTION
    # =====================================

    def handle_execution(
        self,
        data
    ):


        try:

            from execution.execution_engine import execution_engine


            item = data["data"][0]


            execution_engine.on_fill(

                item["symbol"],

                item["side"],

                float(item["execQty"]),

                float(item["execPrice"])

            )


        except Exception as e:


            print(
                "[EXECUTION ERROR]",
                e
            )





    # =====================================
    # POSITION
    # =====================================

    def handle_position(
        self,
        data
    ):


        try:


            item = data["data"][0]


            symbol = item["symbol"]

            size = float(
                item["size"]
            )


            side = item["side"]



            if size > 0:


                position_manager.set_position(

                    symbol,

                    side,

                    size

                )


            else:


                position_manager.remove_position(

                    symbol

                )


        except Exception as e:


            print(
                "[POSITION ERROR]",
                e
            )





    # =====================================
    # WALLET
    # =====================================

    def handle_wallet(
        self,
        data
    ):


        try:


            item = data["data"][0]


            equity = float(

                item.get(

                    "totalEquity",

                    0

                )

            )


            if equity > 0:

                drawdown_guard.update(
                    equity
                )


        except Exception as e:


            print(
                "[WALLET ERROR]",
                e
            )





    def stop(self):

        self.running = False

        self.connected = False



    def status(self):

        return {

            "running": self.running,

            "connected": self.connected

        }





private_ws = PrivateWS()
