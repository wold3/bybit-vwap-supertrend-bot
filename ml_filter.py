import random

class MLModel:
    def __init__(self):
        self.threshold = 0.6

    def predict(self, features):
        return random.random()


model = MLModel()


def should_enter_market(price, volatility, trend_strength):

    score = model.predict({
        "price": price,
        "volatility": volatility,
        "trend_strength": trend_strength
    })

    return score > model.threshold, score
