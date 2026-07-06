import logging

from execution.execution_engine import engine
from risk.risk_engine import risk_engine
from analytics.performance_analyzer import performance_analyzer

logger = logging.getLogger(__name__)


class MultiSymbolEngine:

    def __init__(self):

        self.symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

        self.max_exposure_per_symbol = 1
        self.global_exposure_limit = 3

    # =====================================================
    # Execute Across Symbols
    # =====================================================
    def execute(self, signal_map, qty_map):

        results = {}

        for symbol in self.symbols:

            signal = signal_map.get(symbol)

            qty = qty_map.get(symbol, 0)

            if not signal or qty <= 0:
                continue

            if not risk_engine.allow_trade():
                logger.warning("Risk blocked %s", symbol)
                continue

            logger.info("Executing %s %s", symbol, signal)

            result = engine.execute(
                signal=signal,
                symbol=symbol,
                qty=qty,
                strategy="multi",
                regime="portfolio"
            )

            results[symbol] = result

        return results

    # =====================================================
    # Portfolio PnL
    # =====================================================
    def portfolio_pnl(self):

        stats = performance_analyzer.total_performance()

        return stats.get("total_pnl", 0.0)

    # =====================================================
    # Exposure Check
    # =====================================================
    def exposure_ok(self):

        # 단순 구조 (확장 가능)
        active = len(self.symbols)

        return active <= self.global_exposure_limit


# =====================================================
# Singleton
# =====================================================
multi_engine = MultiSymbolEngine()
