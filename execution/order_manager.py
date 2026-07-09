import time
import uuid

from config import (
    BYBIT_BASE_URL,
    DEFAULT_SYMBOL,
    LIVE_TRADING,
)

from api.bybit_client import bybit_client


class OrderManager:

    def __init__(self):

        self.base = BYBIT_BASE_URL
        self.symbol = DEFAULT_SYMBOL
        self.live = LIVE_TRADING

        # 중복 주문 방지
        self.last_order_time = 0
        self.duplicate_seconds = 3

        print("==============================")
        print("[ORDER MANAGER INIT]")
        print("BASE :", self.base)
        print("LIVE :", self.live)
        print("SYMBOL :", self.symbol)
        print("==============================")

    # =====================================================
    # CREATE ORDER
    # =====================================================

    def create_order(
        self,
        side,
        qty,
        take_profit=None,
        stop_loss=None,
    ):

        now = time.time()

        # -------------------------
        # Duplicate Protection
        # -------------------------

        if now - self.last_order_time < self.duplicate_seconds:

            print("[ORDER BLOCK] DUPLICATE")

            return None

        order_link_id = f"VWAP_{uuid.uuid4().hex[:8]}"

        params = {
            "category": "linear",
            "symbol": self.symbol,
            "side": side,
            "positionIdx": 0,
            "orderType": "Market",
            "qty": str(qty),
            "orderLinkId": order_link_id,
        }

        # -------------------------
        # TP / SL
        # -------------------------

        if take_profit is not None:
            params["takeProfit"] = str(take_profit)

        if stop_loss is not None:
            params["stopLoss"] = str(stop_loss)

        print("==============================")
        print("[ORDER REQUEST]")
        print(params)
        print("==============================")

        try:

            result = bybit_client.post(
                "/v5/order/create",
                params,
            )

            print("[ORDER RESPONSE]", result)

            if result is None:

                print("[ORDER FAILED] NO RESPONSE")

                return None

            if result.get("retCode") != 0:

                print(
                    "[ORDER FAILED]",
                    result.get("retCode"),
                    result.get("retMsg"),
                )

                return result

            # 성공시에만 중복시간 기록
            self.last_order_time = time.time()

            print(
                "[ORDER SUCCESS]",
                order_link_id,
            )

            return result

        except Exception as e:

            print("[ORDER ERROR]", e)

            return None

    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close_position(
        self,
        side,
        qty,
    ):

        close_side = (
            "Sell"
            if side == "Buy"
            else "Buy"
        )

        params = {
            "category": "linear",
            "symbol": self.symbol,
            "side": close_side,
            "positionIdx": 0,
            "orderType": "Market",
            "qty": str(qty),
            "reduceOnly": True,
        }

        print("==============================")
        print("[CLOSE POSITION]")
        print(params)
        print("==============================")

        try:

            result = bybit_client.post(
                "/v5/order/create",
                params,
            )

            print("[CLOSE RESPONSE]", result)

            if result and result.get("retCode") != 0:

                print(
                    "[CLOSE FAILED]",
                    result.get("retCode"),
                    result.get("retMsg"),
                )

            return result

        except Exception as e:

            print("[CLOSE ERROR]", e)

            return None

    # =====================================================
    # CANCEL ALL
    # =====================================================

    def cancel_all(self):

        params = {
            "category": "linear",
            "symbol": self.symbol,
        }

        print("==============================")
        print("[CANCEL ALL]")
        print(params)
        print("==============================")

        try:

            result = bybit_client.post(
                "/v5/order/cancel-all",
                params,
            )

            print("[CANCEL RESPONSE]", result)

            return result

        except Exception as e:

            print("[CANCEL ERROR]", e)

            return None


order_manager = OrderManager()
