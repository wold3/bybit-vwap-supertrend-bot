import threading
import time

from watchdog.watchdog import watchdog


class WSClient:
    """
    Public WebSocket Client

    기능
    - websocket 시작/종료
    - 최신 시세 저장
    - watchdog heartbeat
    """

    def __init__(self):

        self.running = False

        self.thread = None

        # 최신 시장 데이터
        self.latest_data = None

        self.connected = False



    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self.thread.start()

        print("[WS] started")



    def _run(self):

        self.connected = True

        while self.running:

            try:

                # watchdog heartbeat
                watchdog.heartbeat()

                # ===========================
                # TODO
                # Bybit Public WebSocket 연결
                # 수신 데이터는
                # self.update_market_data(data)
                # 호출
                # ===========================

                time.sleep(1)

            except Exception as e:

                print("[WS ERROR]", e)

                time.sleep(5)



        self.connected = False



    def stop(self):

        self.running = False

        self.connected = False

        print("[WS] stopped")



    def update_market_data(self, data):

        """
        websocket에서 호출
        """

        self.latest_data = data



    def get_latest_data(self):

        """
        strategy에서 호출
        """

        return self.latest_data



    def status(self):

        return {

            "running": self.running,

            "connected": self.connected,

            "has_market_data": self.latest_data is not None

        }


# singleton
ws_client = WSClient()
