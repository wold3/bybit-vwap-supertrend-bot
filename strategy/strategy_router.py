import numpy as np
from collections import deque


# =====================================================
# 시장 상태 저장 (간단 ML 대체 레이어)
# =====================================================

price_window = deque(maxlen=50)
volume_window = deque(maxlen=50)


# =====================================================
# 입력 업데이트
# =====================================================

def update_market_state(price, volume=None):

    price_window.append(price)

    if volume is not None:
        volume_window.append(volume)


# =====================================================
# 변동성 계산
# =====================================================

def volatility():

    if len(price_window) < 10:
        return 0.0

    arr = np.array(price_window)

    return float(np.std(arr) / np.mean(arr))


# =====================================================
# 트렌드 판단
# =====================================================

def trend_direction():

    if len(price_window) < 10:
        return "UNKNOWN"

    arr = np.array(price_window)

    short = np.mean(arr[-10:])
    long = np.mean(arr)

    if short > long * 1.002:
        return "TREND_UP"

    if short < long * 0.998:
        return "TREND_DOWN"

    return "RANGE"


# =====================================================
# Fake breakout 필터
# =====================================================

def fake_breakout_filter(price):

    if len(price_window) < 20:
        return True

    arr = np.array(price_window)

    resistance = np.max(arr[-20:])
    support = np.min(arr[-20:])

    # breakout인데 volume 없으면 fake 가능성
    if price > resistance and volatility() < 0.001:
        return False

    if price < support and volatility() < 0.001:
        return False

    return True


# =====================================================
# 신호 신뢰도 점수
# =====================================================

def signal_confidence(price):

    if len(price_window) < 20:
        return 50

    vol = volatility()

    trend = trend_direction()

    confidence = 50

    # 트렌드 가중치
    if trend == "TREND_UP":
        confidence += 20
    elif trend == "TREND_DOWN":
        confidence += 20

    # 변동성 패널티
    if vol > 0.02:
        confidence -= 20

    if vol < 0.005:
        confidence -= 10

    return max(min(confidence, 100), 0)


# =====================================================
# 메인 라우팅
# =====================================================

def route(signal, price):

    update_market_state(price)

    trend = trend_direction()

    confidence = signal_confidence(price)

    # -------------------------
    # fake breakout 차단
    # -------------------------
    if not fake_breakout_filter(price):
        return False, "FAKE_BREAKOUT"

    # -------------------------
    # 신뢰도 필터
    # -------------------------
    if confidence < 40:
        return False, "LOW_CONFIDENCE"

    # -------------------------
    # 기본 필터
    # -------------------------
    if trend == "UNKNOWN":
        return False, "NO_TREND"

    return True, trend


# =====================================================
# Helper
# =====================================================

def get_state():

    return {
        "trend": trend_direction(),
        "volatility": volatility(),
        "confidence": signal_confidence(price_window[-1] if price_window else 0),
        "last_price": price_window[-1] if price_window else None,
    }
