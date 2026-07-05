class Metrics:

    def __init__(self):
        self.prices = []

    def update(self, price):

        self.prices.append(price)

        if len(self.prices) > 1000:
            self.prices.pop(0)

    def volatility(self):

        if len(self.prices) < 2:
            return 0.0

        mean = sum(self.prices) / len(self.prices)

        return sum((p - mean) ** 2 for p in self.prices) / len(self.prices)

    def trend(self):

        if len(self.prices) < 10:
            return 0.0

        return self.prices[-1] - self.prices[0]
