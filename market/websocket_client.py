# market/websocket_client.py

import json
import time
import threading
import websocket

from dotenv import load_dotenv
import os

load_dotenv()


class BybitWebSocket:

    def __init__(
        self,
        symbol="BTCUSDT",
        interval="1",
        callback=None
    ):

        self.symbol = symbol
        self.interval = interval
        self.callback = callback

        self.ws = None
        self.connected = False
        self.running = False

        self.url = os.getenv(
            "BYBIT_PUBLIC_WS",
            "wss://stream-demo.bybit.com/v5/public/linear"
        )

    # ==============================
    # START
    # ==============================

    def start(self):

        if self.running:
            return

        self.running = True

        thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        thread.start()

    # ==============================
    # LOOP
    # ==============================

    def _run(self):

        while self.running:

            try:

                self.ws = websocket.WebSocketApp(

                    self.url,

                    on_open=self.on_open,

                    on_message=self.on_message,

                    on_error=self.on_error,

                    on_close=self.on_close

                )

                self.ws.run_forever(
                    ping_interval=20,
                    ping_timeout=10
                )

            except Exception as e:

                print("[WS ERROR]", e)

            print("[WS] reconnect in 5 sec...")
            time.sleep(5)

    # ==============================
    # OPEN
    # ==============================

    def on_open(
        self,
        ws
    ):

        self.connected = True

        print("[WS CONNECTED]")

        sub = {

            "op": "subscribe",

            "args": [

                f"kline.{self.interval}.{self.symbol}"

            ]

        }

        ws.send(json.dumps(sub))

    # ==============================
    # MESSAGE
    # ==============================

    def on_message(
        self,
        ws,
        message
    ):

        try:

            data = json.loads(message)

        except Exception:

            return

        if "topic" not in data:
            return

        if not data["topic"].startswith("kline"):
            return

        candles = data.get("data", [])

        for candle in candles:

            if self.callback:

                self.callback(candle)

    # ==============================
    # ERROR
    # ==============================

    def on_error(
        self,
        ws,
        error
    ):

        print("[WS ERROR]", error)

    # ==============================
    # CLOSE
    # ==============================

    def on_close(
        self,
        ws,
        code,
        msg
    ):

        self.connected = False

        print("[WS CLOSED]", code, msg)

    # ==============================
    # STOP
    # ==============================

    def stop(self):

        self.running = False

        if self.ws:

            self.ws.close()


# =====================================
# TEST
# =====================================

if __name__ == "__main__":

    def print_candle(candle):

        print(
            candle["start"],
            candle["close"]
        )

    ws = BybitWebSocket(
        symbol="BTCUSDT",
        interval="1",
        callback=print_candle
    )

    ws.start()

    while True:
        time.sleep(1)
