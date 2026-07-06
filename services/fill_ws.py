import asyncio
import json
import websockets
import os

from portfolio.position_manager import position_manager
from telegram import telegram


class FillTracker:

    def __init__(self):

        self.url = "wss://stream.bybit.com/v5/private"

    # =================================================
    # MAIN LOOP
    # =================================================
    async def connect(self):

        async with websockets.connect(self.url) as ws:

            # 로그인 (Private WS)
            await self.auth(ws)

            # 체결 구독
            subscribe_msg = {
                "op": "subscribe",
                "args": ["execution"]
            }

            await ws.send(json.dumps(subscribe_msg))

            print("[FILL WS] CONNECTED")

            while True:

                msg = await ws.recv()
                data = json.loads(msg)

                self.handle(data)

    # =================================================
    # AUTH
    # =================================================
    async def auth(self, ws):

        import time, hmac, hashlib

        api_key = os.getenv("BYBIT_API_KEY")
        api_secret = os.getenv("BYBIT_API_SECRET")

        timestamp = str(int(time.time() * 1000))

        payload = f"GET/realtime{timestamp}"

        sign = hmac.new(
            api_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

        auth_msg = {
            "op": "auth",
            "args": [api_key, timestamp, sign]
        }

        await ws.send(json.dumps(auth_msg))

    # =================================================
    # HANDLE EXECUTION (FILL)
    # =================================================
    def handle(self, data):

        try:
            if "data" not in data:
                return

            fills = data["data"]

            if isinstance(fills, list):

                for f in fills:

                    symbol = f.get("symbol")
                    side = f.get("side")
                    qty = float(f.get("execQty", 0))
                    price = float(f.get("execPrice", 0))

                    print(f"[FILL] {symbol} {side} {qty}@{price}")

                    # ============================
                    # POSITION UPDATE
                    # ============================
                    position_manager.update_fill(
                        symbol=symbol,
                        side=side,
                        qty=qty,
                        price=price
                    )

                    # ============================
                    # ALERT
                    # ============================
                    telegram.send(
                        f"📌 FILL EXECUTED\n"
                        f"{symbol} {side}\n"
                        f"Qty: {qty}\nPrice: {price}"
                    )

        except Exception as e:
            print("[FILL ERROR]", e)


# SINGLETON RUNNER
def start_fill_ws():

    tracker = FillTracker()
    asyncio.run(tracker.connect())
