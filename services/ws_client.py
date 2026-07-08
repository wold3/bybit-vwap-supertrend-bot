import threading
import time

from watchdog.watchdog import watchdog


class WSClient:
    """
    Public WebSocket Client
    """

    def __init__(self):

        self.running = False
        self.connected = False
        self.thread = None

        self.latest_data = None
        self.last_update = 0


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

                watchdog.heartbeat()

                # TODO:
                # 실제 Bybit WebSocket 연결 후
                # self.update_market_data(data) 호출

                # 테스트용 더미 데이터
                if self.latest_data is None:

                    self.update_market_data({

                        "symbol": "BTCUSDT",

                        "price": 0,

                        "timestamp": time.time()

                    })

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

        self.latest_data = data
        self.last_update = time.time()


    def get_latest_data(self):

        return self.latest_data


    def is_connected(self):

        return self.connected


    def status(self):

        return {

            "running": self.running,

            "connected": self.connected,

            "has_market_data": self.latest_data is not None,

            "last_update": self.last_update

        }


ws_client = WSClient()
