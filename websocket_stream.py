import threading
from pybit.unified_trading import WebSocket

from state import sync_real_pnl

ws = None


def start_ws(symbol="BTCUSDT"):
    """
    Bybit WebSocket 실시간 PnL / Position sync
    """

    def handle_message(message):
        try:
            # 메시지 들어올 때마다 PnL sync
            sync_real_pnl(symbol)

        except Exception as e:
            print("WS error:", e)


    def run():

        global ws

        ws = WebSocket(
            testnet=False,
            channel_type="linear"
        )

        # 포지션 스트림
        ws.position_stream(callback=handle_message)

        # 거래 스트림
        ws.trade_stream(callback=handle_message)


    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
