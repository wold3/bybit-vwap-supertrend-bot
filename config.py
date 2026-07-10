import os


# =====================================================
# MODE
# =====================================================

# 실제 주문 실행 여부
# False = 주문 차단 (테스트)
# True  = Demo 주문 실행
LIVE_TRADING = True


# Bybit Demo Trading
DEMO_TRADING = True


# Bybit Testnet 사용 여부
TESTNET = False





# =====================================================
# API KEY
# =====================================================

BYBIT_API_KEY = os.getenv(
    "BYBIT_API_KEY",
    "YOUR_DEMO_API_KEY"
)


BYBIT_API_SECRET = os.getenv(
    "BYBIT_API_SECRET",
    "YOUR_DEMO_API_SECRET"
)





# =====================================================
# ACCOUNT
# =====================================================

ACCOUNT_TYPE = "UNIFIED"





# =====================================================
# MARKET
# =====================================================

DEFAULT_SYMBOL = "BTCUSDT"

CATEGORY = "linear"


TIMEFRAME = "1"







# =====================================================
# REST API
# =====================================================

if DEMO_TRADING:


    # Demo Trading API

    BYBIT_BASE_URL = (
        "https://api-demo.bybit.com"
    )


elif TESTNET:


    BYBIT_BASE_URL = (
        "https://api-testnet.bybit.com"
    )


else:


    BYBIT_BASE_URL = (
        "https://api.bybit.com"
    )









# =====================================================
# WEBSOCKET
# =====================================================

if DEMO_TRADING:


    # Private WS
    BYBIT_PRIVATE_WS = (
        "wss://stream-demo.bybit.com/v5/private"
    )


    # Public market data
    # Demo Public WS는 일부 환경에서 404 발생 가능
    # 시장 데이터용으로 일반 Public WS 사용

    BYBIT_PUBLIC_WS = (
        "wss://stream.bybit.com/v5/public/linear"
    )



elif TESTNET:


    BYBIT_PUBLIC_WS = (
        "wss://stream-testnet.bybit.com/v5/public/linear"
    )


    BYBIT_PRIVATE_WS = (
        "wss://stream-testnet.bybit.com/v5/private"
    )



else:


    BYBIT_PUBLIC_WS = (
        "wss://stream.bybit.com/v5/public/linear"
    )


    BYBIT_PRIVATE_WS = (
        "wss://stream.bybit.com/v5/private"
    )









# =====================================================
# TRADING
# =====================================================

LEVERAGE = 5


DEFAULT_QTY = 0.001







# =====================================================
# INDICATOR
# =====================================================

VWAP_LENGTH = 20


SUPERTREND_PERIOD = 10


SUPERTREND_MULTIPLIER = 3









# =====================================================
# RISK
# =====================================================

MAX_POSITION_SIZE = 0.01


DAILY_LOSS_LIMIT = -100


ORDER_COOLDOWN = 30







# =====================================================
# LOG
# =====================================================

LOG_LEVEL = "INFO"





print("==============================")
print("[CONFIG LOADED]")
print("DEMO :", DEMO_TRADING)
print("TESTNET :", TESTNET)
print("LIVE :", LIVE_TRADING)
print("ACCOUNT :", ACCOUNT_TYPE)
print("SYMBOL :", DEFAULT_SYMBOL)
print("REST :", BYBIT_BASE_URL)
print("PUBLIC WS :", BYBIT_PUBLIC_WS)
print("PRIVATE WS :", BYBIT_PRIVATE_WS)
print("==============================")
