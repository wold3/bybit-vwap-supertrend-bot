import logging

from analytics.performance_analyzer import performance_analyzer

logger = logging.getLogger(__name__)


class AutoTuner:

    def __init__(self):

        self.weights = {
            "trend": 1.0,
            "range": 1.0,
            "safe": 1.0,
        }

    # =====================================================
    # Update Weights
    # =====================================================
    def tune(self):

        stats = performance_analyzer.analyze_by_strategy()

        for strategy, data in stats.items():

            pnl = data["pnl"]
            win_rate = data["win_rate"]

            # 기본 규칙
            if win_rate >= 60 and pnl > 0:
                self.weights[strategy] = min(
                    self.weights.get(strategy, 1.0) + 0.1,
                    2.0
                )

            elif win_rate < 40 or pnl < 0:
                self.weights[strategy] = max(
                    self.weights.get(strategy, 1.0) - 0.1,
                    0.2
                )

        logger.info("Auto tuning completed: %s", self.weights)

    # =====================================================
    # Get Weight
    # =====================================================
    def get_weight(self, strategy):

        return self.weights.get(strategy, 1.0)

    # =====================================================
    # Apply Weight
    # =====================================================
    def adjust_signal_strength(self, strategy, base_signal):

        weight = self.get_weight(strategy)

        if weight < 0.5:
            return "WEAK"

        if weight > 1.5:
            return "STRONG"

        return base_signal

    # =====================================================
    # Status
    # =====================================================
    def status(self):

        return {
            "weights": self.weights,
        }


# =====================================================
# Singleton
# =====================================================
auto_tuner = AutoTuner()
