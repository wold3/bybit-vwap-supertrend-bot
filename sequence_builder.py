from collections import deque
from feature_engine import get_feature_vector

SEQ = deque(maxlen=20)


def build_sequence(price, orderbook=None):

    feat = get_feature_vector(price, orderbook)

    SEQ.append(feat)

    if len(SEQ) < 20:
        return list(SEQ) * (20 // len(SEQ))

    return list(SEQ)
