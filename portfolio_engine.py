class Portfolio:

    def __init__(self):
        self.strategies = {
            "trend": {"capital": 400},
            "range": {"capital": 300},
            "safe": {"capital": 300}
        }

    def allocate(self, regime):

        if regime == "TREND_UP":
            return "trend"

        if regime == "RANGE":
            return "range"

        return "safe"


portfolio = Portfolio()
