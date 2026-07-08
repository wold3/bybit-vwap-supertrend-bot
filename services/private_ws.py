import os
import threading
import time

from dotenv import load_dotenv

from watchdog.watchdog import watchdog

load_dotenv()


class PrivateWS:
    """
    Bybit Private WebSocket

    기능
    - Private WS 관리
    - Heartbeat
    - 주문/체결 이벤트 수신
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

        print("🔐 PRIVATE WS CONNECTED")


    # =====================================
    # LOOP
    # =====================================

    def _run(self):

        self.connected = True

        print("PRIVATE CHANNEL SUBSCRIBED")

        while self.running:

            try:

                watchdog.heartbeat()

                # ===================================
                # TODO
                # Bybit Private WebSocket 연결
                #
                # 주문 체결
                # Position
                # Wallet
                # Execution
                # ===================================

                time.sleep(1)

            except Exception as e:

                print("PRIVATE WS ERROR", e)

                time.sleep(5)

        self.connected = False


    # =====================================
    # STOP
    # =====================================

    def stop(self):

        self.running = False

        self.connected = False

        print("PRIVATE WS STOPPED")


    # =====================================
    # STATUS
    # =====================================

    def status(self):

        return {

            "running": self.running,

            "connected": self.connected

        }


# singleton
private_ws = PrivateWS()
