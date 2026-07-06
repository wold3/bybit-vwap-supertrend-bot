import asyncio
import json
import websockets

from strategy.strategy_engine import run_strategy


class BybitWSClient:

    def __init__(self, url, engine):

        self.url = url
        self.engine = engine

    # =================================================
    # MAIN LOOP
    # =================================================
    async def connect(self):

        async with websockets.connect(self.url) as ws:

            # 🔥 구독 메시지 (Bybit v5)
            subscribe_msg = {
                "op": "subscribe",
                "args": [
                    "publicTrade.BTCUSDT"
                ]
            }

            await ws.send(json.dumps(subscribe_msg))

            print("[WS] CONNECTED")

            while True:

                try:
                    msg = await ws.recv()
                    data = json.loads(msg)

                    self.handle(data)

                except Exception as e:
                    print("[WS ERROR]", e)

    # =================================================
    # HANDLE MESSAGE
    # =================================================
    def handle(self, data):

        # Bybit trade stream 구조
        if "data" in data:

            trades = data["data"]

            if isinstance(trades, list) and len(trades) > 0:

                last_price = float(trades[-1]["p"])

                # 🔥 전략 엔진 호출 (실시간)
                self.engine.on_price(last_price)


# SINGLETON RUNNER
def start_ws(engine):

    import os

    url = os.getenv("BYBIT_WS_URL")

    client = BybitWSClient(url, engine)

    asyncio.run(client.connect())
