class Portfolio:
    """
    전략별 자본 및 성과 관리
    """

    def __init__(self):

        self.strategies = {

            "trend": {
                "capital": 400.0,
                "pnl": 0.0,
                "trades": 0,
                "wins": 0,
                "losses": 0,
            },

            "range": {
                "capital": 300.0,
                "pnl": 0.0,
                "trades": 0,
                "wins": 0,
                "losses": 0,
            },

            "safe": {
                "capital": 300.0,
                "pnl": 0.0,
                "trades": 0,
                "wins": 0,
                "losses": 0,
            },
        }

    # ----------------------------------
    # 전략 선택
    # ----------------------------------

    def allocate(self, regime):

        regime = regime.upper()

        if regime == "TREND_UP":
            return "trend"

        if regime == "TREND_DOWN":
            return "trend"

        if regime == "RANGE":
            return "range"

        return "safe"

    # ----------------------------------
    # 거래 결과 반영
    # ----------------------------------

    def update(self, strategy, pnl):

        if strategy not in self.strategies:
            return

        s = self.strategies[strategy]

        pnl = float(pnl)

        s["pnl"] += pnl
        s["capital"] += pnl
        s["trades"] += 1

        if pnl >= 0:
            s["wins"] += 1
        else:
            s["losses"] += 1

    # ----------------------------------
    # 전략 정보
    # ----------------------------------

    def get(self, strategy):

        return self.strategies.get(strategy)

    # ----------------------------------
    # 전체 자산
    # ----------------------------------

    def total_capital(self):

        return round(

            sum(
                s["capital"]
                for s in self.strategies.values()
            ),

            2,
        )

    # ----------------------------------
    # 승률
    # ----------------------------------

    def win_rate(self, strategy):

        s = self.strategies.get(strategy)

        if not s:
            return 0.0

        trades = s["trades"]

        if trades == 0:
            return 0.0

        return round(
            s["wins"] / trades * 100,
            2,
        )

    # ----------------------------------
    # 상태 조회
    # ----------------------------------

    def summary(self):

        result = {}

        for name in self.strategies:

            s = self.strategies[name]

            result[name] = {

                "capital": round(s["capital"], 2),

                "pnl": round(s["pnl"], 2),

                "trades": s["trades"],

                "wins": s["wins"],

                "losses": s["losses"],

                "win_rate": self.win_rate(name),
            }

        result["total_capital"] = self.total_capital()

        return result


portfolio = Portfolio()
