import logging
from api.bybit_client import bybit_client
from portfolio.position_manager import position_manager

logger = logging.getLogger(__name__)


class SyncEngine:

    def __init__(self):
        self.last_sync_price = None

    # =====================================================
    # 포지션 sync
    # =====================================================
    def sync(self, symbol):

        try:

            resp = bybit_client._request(
                "GET",
                "/v5/position/list",
                {"category": "linear", "symbol": symbol}
            )

            if not isinstance(resp, dict):
                return

            result = resp.get("result", {})
            list_data = result.get("list", [])

            if not list_data:
                position_manager.position = None
                return

            pos = list_data[0]

            size = float(pos.get("size", 0))
            if size == 0:
                position_manager.position = None
                return

            side = pos.get("side")
            entry_price = float(pos.get("avgPrice", 0))

            # -------------------------
            # 내부 state override
            # -------------------------
            position_manager.position = {
                "symbol": symbol,
                "side": side,
                "qty": size,
                "entry_price": entry_price,
                "unrealized_pnl": float(pos.get("unrealisedPnl", 0))
            }

            logger.info(f"SYNC POSITION: {side} {size} @ {entry_price}")

        except Exception as e:
            logger.error(f"SYNC ERROR: {str(e)}")


sync_engine = SyncEngine()
