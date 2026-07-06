import logging
from decimal import Decimal

from api.bybit_api import execute_market
from risk.risk_engine import risk_engine

from database.repository import add_trade

logger = logging.getLogger(__name__)


# =====================================================
# 포지션 사이징 (실전용: equity 기반 + 리스크 반영)
# =====================================================

def position_size(equity, risk_score, win_rate):

    base_risk = 0.02  # 2%

    if risk_score < 40:
        base_risk = 0.005

    if win_rate > 60:
        base_risk *= 1.2

    if win_rate < 45:
        base_risk *= 0.5

    qty = equity * base_risk

    return round(qty, 4)


# =====================================================
# 레버리지 계산 (안정 + 수익 균형)
# =====================================================

def calc_leverage(risk_score, win_rate):

    if risk_score < 30:
        return 1

    if win_rate > 60 and risk_score > 70:
        return 5

    if win_rate > 50:
        return 3

    if risk_score > 50:
        return 2

    return 1


# =====================================================
# 실거래 실행
# =====================================================

def execute_order(signal, symbol, price, equity, win_rate):

    risk_score = risk_engine.risk_score()

    # -------------------------
    # 리스크 차단
    # -------------------------
    if not risk_engine.allow_trade():
        logger.warning("TRADE BLOCKED by risk engine")
        return {
            "success": False,
            "reason": "risk_block",
        }

    # -------------------------
    # sizing & leverage
    # -------------------------
    qty = position_size(equity, risk_score, win_rate)
    leverage = calc_leverage(risk_score, win_rate)

    try:

        # Bybit 주문 실행 (시장가)
        order = execute_market(
            side=signal,
            symbol=symbol,
            qty=qty,
            leverage=leverage
        )

        # -------------------------
        # DB 저장
        # -------------------------
        trade = add_trade(
            symbol=symbol,
            side=signal,
            qty=qty,
            price=price,
            leverage=leverage,
        )

        logger.info(
            f"[TRADE] {signal} {symbol} qty={qty} lev={leverage}"
        )

        return {
            "success": True,
            "order": order,
            "trade_id": trade.id,
            "qty": qty,
            "leverage": leverage,
            "risk_score": risk_score,
        }

    except Exception as e:

        logger.error(f"EXECUTION ERROR: {str(e)}")

        return {
            "success": False,
            "reason": "execution_error",
            "error": str(e),
        }
