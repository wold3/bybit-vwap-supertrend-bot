import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class SelfLearningEngine:

    def __init__(self):

        # strategy performance tracking
        self.stats = defaultdict(lambda: {
            "wins": 0,
            "losses": 0,
            "pnl": 0.0
        })

    # =====================================================
    # Update Result
    # =====================================================
    def update(self, strategy, pnl):

        s = self.stats[strategy]

        s["pnl"] += pnl

        if pnl > 0:
            s["wins"] += 1
        else:
            s["losses"] += 1

        logger.info(
            "Strategy update %s pnl=%s",
            strategy,
            pnl
        )

    # =====================================================
    # Score Calculation
    # =====================================================
    def score(self, strategy):

        s = self.stats[strategy]

        total = s["wins"] + s["losses"]

        if total == 0:
            return 0.0

        win_rate = s["wins"] / total

        avg_pnl = s["pnl"] / total

        return round(
            win_rate * 0.7 + avg_pnl * 0.3,
            4
        )

    # =====================================================
    # Best Strategy
    # =====================================================
    def best_strategy(self):

        if not self.stats:
            return None

        best = None
        best_score = -999

        for strategy in self.stats:

            score = self.score(strategy)

            if score > best_score:
                best_score = score
                best = strategy

        return best

    # =====================================================
    # Suggest Strategy
    # =====================================================
    def suggest(self, default="trend"):

        best = self.best_strategy()

        if not best:
            return default

        return best

    # =====================================================
    # Report
    # =====================================================
    def report(self):

        return {
            strategy: {
                "score": self.score(strategy),
                **self.stats[strategy]
            }
            for strategy in self.stats
        }


# =====================================================
# Singleton
# =====================================================
self_learning_engine = SelfLearningEngine()
