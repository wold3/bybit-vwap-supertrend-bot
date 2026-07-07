import threading
import time


from watchdog import watchdog



class WSClient:

    def __init__(self):

        self.running = False
        self.thread = None



    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        self.thread.start()

        print("[WSClient] started")



    def run(self):

        while self.running:

            try:

                # watchdog heartbeat
                watchdog.heartbeat()


                # TODO:
                # 여기에 Bybit WebSocket 연결 코드 추가


                time.sleep(5)


            except Exception as e:

                print(
                    "[WSClient ERROR]",
                    e
                )

                time.sleep(5)



    def stop(self):

        self.running = False

        print("[WSClient] stopped")



    def status(self):

        return {
            "running": self.running
        }



# singleton

ws_client = WSClient()
