import logging

from ai.market_regime_model import market_regime_model
from risk.risk_engine import risk_engine
from strategy.strategy_wrapper import execute_strategy

logger = logging.getLogger(__name__)


class AutoStrategySelector:

    def __init__(self):

        self.last_decision = None

    # =====================================================
    # Final Decision Engine
    # =====================================================
    def decide(
        self,
        candles,
        signal,
        price,
        symbol=None,
        qty=None,
    ):

        # ----------------------------
        # 1. Market Regime
        # ----------------------------
        regime = market_regime_model.predict(candles)

        # ----------------------------
        # 2. Risk Check
        # ----------------------------
        if not risk_engine.allow_trade():

            logger.warning("Blocked by risk engine")

            return {
                "success": False,
                "reason": "risk_block",
                "regime": regime,
            }

        # ----------------------------
        # 3. Strategy Selection
        # ----------------------------
        strategy_result = execute_strategy(
            signal=signal,
            price=price,
            symbol=symbol,
            qty=qty,
        )

        if not strategy_result.get("success"):

            return {
                "success": False,
                "reason": strategy_result.get("reason"),
                "regime": regime,
            }

        strategy = strategy_result["strategy"]

        # ----------------------------
        # 4. Regime Filter Override
        # ----------------------------

        if regime == "VOLATILE":

            return {
                "success": False,
                "reason": "volatility_filter",
                "regime": regime,
            }

        if regime == "TREND_UP" and strategy == "range":

            strategy = "trend"

        if regime == "TREND_DOWN":

            strategy = "short"

        # ----------------------------
        # 5. Final Decision
        # ----------------------------
        decision = {
            "success": True,
            "strategy": strategy,
            "regime": regime,
            "signal": signal,
            "symbol": symbol,
            "qty": qty,
        }

        self.last_decision = decision

        return decision

    # =====================================================
    # Quick Check
    # =====================================================
    def can_trade(self, candles, signal, price):

        return self.decide(
            candles,
            signal,
            price
        )["success"]


# =====================================================
# Singleton
# =====================================================
auto_selector = AutoStrategySelector()
