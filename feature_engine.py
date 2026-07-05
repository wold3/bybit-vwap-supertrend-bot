import random

def get_features(symbol, price):

    return {
        "volatility": random.random(),
        "trend_strength": random.random(),
        "price_action": "normal"
    }
