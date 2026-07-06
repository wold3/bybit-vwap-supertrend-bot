from collections import defaultdict
from datetime import datetime

from database.repository import get_recent_trades


class PerformanceAnalyzer:

    def __init__(self):

        self.cache = {}

    # =====================================================
    # Load Trades
    # =====================================================
    def load_trades(self, limit=500):

        return get_recent_trades(limit)

    # =====================================================
    # Strategy Performance
    # =====================================================
    def analyze_by_strategy(self):

        trades = self.load_trades()

        stats = defaultdict(lambda: {
            "pnl": 0.0,
            "wins": 0,
            "losses": 0,
            "count": 0
        })

        for t in trades:

            strategy = getattr(t, "strategy", "unknown")

            pnl = float(getattr(t, "pnl", 0))

            stats[strategy]["pnl"] += pnl
            stats[strategy]["count"] += 1

            if pnl > 0:
                stats[strategy]["wins"] += 1
            else:
                stats[strategy]["losses"] += 1

        # calculate win rate
        for k, v in stats.items():

            if v["count"] > 0:
                v["win_rate"] = round(
                    v["wins"] / v["count"] * 100,
                    2
                )
            else:
                v["win_rate"] = 0.0

        return dict(stats)

    # =====================================================
    # Total Performance
    # =====================================================
    def total_performance(self):

        trades = self.load_trades()

        total_pnl = sum(float(t.pnl or 0) for t in trades)

        wins = len([t for t in trades if float(t.pnl or 0) > 0])
        losses = len([t for t in trades if float(t.pnl or 0) <= 0])

        win_rate = (wins / len(trades) * 100) if trades else 0

        return {
            "total_pnl": round(total_pnl, 2),
            "trades": len(trades),
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 2),
        }

    # =====================================================
    # Health Check Strategy
    # =====================================================
    def is_strategy_healthy(self, strategy_name):

        stats = self.analyze_by_strategy()

        if strategy_name not in stats:
            return False

        s = stats[strategy_name]

        # 기준
        if s["win_rate"] < 40:
            return False

        if s["pnl"] < -50:
            return False

        return True

    # =====================================================
    # Daily Report
    # =====================================================
    def daily_report(self):

        stats = self.total_performance()

        return {
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "performance": stats
        }


# =====================================================
# Singleton
# =====================================================
performance_analyzer = PerformanceAnalyzer()
