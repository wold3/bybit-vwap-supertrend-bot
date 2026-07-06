import time
import logging
from datetime import datetime

from api.bybit_client import bybit_client

logger = logging.getLogger(__name__)


# =====================================================
# Side 변환 (핵심 수정)
# =====================================================

def normalize_side(signal: str):

    if not signal:
        return None

    signal = signal.lower()

    if signal in ["buy", "long", "up", "bull", "bullish"]:
        return "Buy"

    if signal in ["sell", "short", "down", "bear", "bearish"]:
        return "Sell"

    return None


# =====================================================
# Order Manager
# =====================================================

class OrderManager:

    def __init__(self):
        self.open_orders = {}
        self.filled_orders = {}

    # =====================================================
    # 주문 생성
    # =====================================================

    def place_market_order(self, symbol, side, qty, leverage=1):

        try:
            side = normalize_side(side)

            if side is None:
                logger.error(f"INVALID SIDE SIGNAL: {side}")
                return None

            resp = bybit_client.place_order(
                symbol=symbol,
                side=side,
                qty=qty,
                leverage=leverage
            )

            logger.info(f"BYBIT RESPONSE: {resp}")

            if not isinstance(resp, dict):
                logger.error(f"Invalid response type: {type(resp)}")
                return None

            result = resp.get("result", {})
            order_id = result.get("orderId")

            if not order_id:
                logger.error(f"Order failed (no orderId): {resp}")
                return None

            self.open_orders[order_id] = {
                "symbol": symbol,
                "side": side,
                "qty": qty,
                "status": "PENDING",
                "created_at": datetime.utcnow()
            }

            logger.info(f"ORDER PLACED: {order_id}")

            return order_id

        except Exception as e:
            logger.error(f"Place order error: {str(e)}")
            return None

    # =====================================================
    # 주문 상태 확인
    # =====================================================

    def check_order_status(self, order_id):

        order = self.open_orders.get(order_id)

        if not order:
            return None

        if (datetime.utcnow() - order["created_at"]).seconds > 2:

            order["status"] = "FILLED"
            self.filled_orders[order_id] = order
            del self.open_orders[order_id]

            return "FILLED"

        return "PENDING"

    # =====================================================
    # 전체 오픈 주문 체크
    # =====================================================

    def sync_orders(self):

        for order_id in list(self.open_orders.keys()):

            status = self.check_order_status(order_id)

            if status == "FILLED":
                logger.info(f"ORDER FILLED: {order_id}")

    # =====================================================
    # 실패 주문 재시도
    # =====================================================

    def retry_failed_order(self, symbol, side, qty, leverage=1):

        logger.warning("Retrying failed order...")

        return self.place_market_order(symbol, side, qty, leverage)

    # =====================================================
    # 상태 조회
    # =====================================================

    def status(self):

        return {
            "open_orders": len(self.open_orders),
            "filled_orders": len(self.filled_orders)
        }


# =====================================================
# SINGLETON
# =====================================================

order_manager = OrderManager()
