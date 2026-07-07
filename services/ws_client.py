import threading
import time


# GitHub 구조 호환 import
from watchdog import watchdog



class WSClient:
    """
    WebSocket Client Manager

    기능:
    - websocket 서비스 상태 관리
    - heartbeat 전송
    - watchdog 연동
    """


    def __init__(self):

        self.running = False
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

        print("[WS] started")



    def _run(self):

        while self.running:

            try:

                # watchdog heartbeat
                watchdog.heartbeat()


                # websocket 처리 위치
                # TODO:
                # Bybit websocket 연결 코드 추가


                time.sleep(5)


            except Exception as e:

                print(
                    "[WS ERROR]",
                    e
                )

                time.sleep(5)



    def stop(self):

        self.running = False

        print("[WS] stopped")



    def status(self):

        return {
            "running": self.running
        }



# 외부 import용 singleton

ws_client = WSClient()
