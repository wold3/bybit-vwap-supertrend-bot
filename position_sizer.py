from config import (
    RISK_PER_TRADE,
    MIN_ORDER_QTY,
    MAX_ORDER_QTY,
)

try:
    from bybit_api import get_balance
except ImportError:
    get_balance = None


def account_balance():
    """
    계좌 잔고 조회
    """

    if get_balance is None:
        return 1000.0

    try:
        result = get_balance()

        if isinstance(result, dict):
            wallet = (
                result.get("result", {})
                      .get("list", [])
            )

            if wallet:
                coin = wallet[0].get("coin", [])

                if coin:
                    return float(
                        coin[0].get("walletBalance", 1000)
                    )

    except Exception:
        pass

    return 1000.0


def calculate_qty(entry_price, stop_loss):
    """
    리스크 기반 주문 수량 계산
    """

    entry_price = float(entry_price)
    stop_loss = float(stop_loss)

    if entry_price <= 0:
        raise ValueError("entry_price must be greater than zero.")

    distance = abs(entry_price - stop_loss)

    if distance <= 0:
        return MIN_ORDER_QTY

    balance = account_balance()

    risk_amount = balance * RISK_PER_TRADE

    qty = risk_amount / distance

    qty = max(MIN_ORDER_QTY, qty)
    qty = min(MAX_ORDER_QTY, qty)

    return round(qty, 6)


def estimate_risk(entry_price, stop_loss):
    """
    예상 손실 금액 계산
    """

    qty = calculate_qty(entry_price, stop_loss)

    return round(
        qty * abs(entry_price - stop_loss),
        2
    )


def get_position_info(entry_price, stop_loss):
    """
    주문 정보 반환
    """

    qty = calculate_qty(entry_price, stop_loss)

    return {
        "balance": account_balance(),
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "qty": qty,
        "estimated_risk": estimate_risk(
            entry_price,
            stop_loss,
        ),
    }
