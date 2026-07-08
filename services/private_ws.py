import threading
import time


from watchdog.watchdog import watchdog

from execution.execution_engine import execution_engine

from position.position_manager import position_manager

from risk.drawdown_guard import drawdown_guard



class PrivateWS:
    """
    Bybit Private WebSocket

    기능:
    - Private WS 관리
    - 주문 체결 이벤트 처리
    - Position 업데이트
    - Wallet 업데이트
    """



    def __init__(self):

        self.running = False

        self.connected = False

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
            "🔐 PRIVATE WS START"
        )





    # =====================================
    # LOOP
    # =====================================

    def _run(self):


        self.connected = True


        print(
            "PRIVATE CHANNEL SUBSCRIBED"
        )



        while self.running:


            try:


                watchdog.heartbeat()



                # =================================
                # 실제 Bybit Private WS 위치
                #
                # 수신 예:
                #
                # order
                # execution
                # position
                # wallet
                #
                # self.handle_message(data)
                #
                # =================================



                time.sleep(1)



            except Exception as e:


                print(

                    "PRIVATE WS ERROR",

                    e

                )


                time.sleep(5)



        self.connected = False





    # =====================================
    # MESSAGE HANDLER
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
    # EXECUTION EVENT
    # =====================================

    def handle_execution(
        self,
        data
    ):


        try:


            item = data["data"][0]



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



            execution_engine.on_fill(

                symbol,

                side,

                qty,

                price

            )



        except Exception as e:


            print(

                "[EXECUTION HANDLE ERROR]",

                e

            )





    # =====================================
    # POSITION EVENT
    # =====================================

    def handle_position(
        self,
        data
    ):


        try:


            item = data["data"][0]



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

                    size

                )


            else:


                position_manager.close_position(

                    symbol

                )



        except Exception as e:


            print(

                "[POSITION HANDLE ERROR]",

                e

            )





    # =====================================
    # WALLET EVENT
    # =====================================

    def handle_wallet(
        self,
        data
    ):


        try:


            equity = float(

                data["data"][0]

                .get(

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

                "[WALLET HANDLE ERROR]",

                e

            )





    # =====================================
    # STOP
    # =====================================

    def stop(self):


        self.running = False

        self.connected = False


        print(
            "PRIVATE WS STOPPED"
        )





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





# singleton

private_ws = PrivateWS()
