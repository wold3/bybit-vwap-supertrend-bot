"""
Production Safety Configuration
실거래 운영 안정화 설정
"""

# =====================================================
# Trading Limits
# =====================================================

MAX_TRADES_PER_MINUTE = 3
MAX_TRADES_PER_HOUR = 30

MAX_DAILY_LOSS = 100  # USDT 기준
MAX_CONSECUTIVE_LOSSES = 5

MAX_POSITION_PER_SYMBOL = 1
MAX_GLOBAL_POSITIONS = 3

# =====================================================
# Risk Control
# =====================================================

ENABLE_RISK_ENGINE = True
ENABLE_AUTO_REDUCE_EXPOSURE = True

# 손실 발생 시 거래 중지
AUTO_STOP_ON_DRAWDOWN = True
DRAWDOWN_LIMIT = 0.1  # 10%

# =====================================================
# Execution Safety
# =====================================================

ENABLE_EXECUTION_LOCK = True
ORDER_RETRY_LIMIT = 3
ORDER_TIMEOUT_SEC = 5

SLIPPAGE_LIMIT = 0.003  # 0.3%

# =====================================================
# API Protection
# =====================================================

API_RATE_LIMIT_PER_SEC = 10
API_BURST_LIMIT = 20

ENABLE_API_BACKOFF = True

# =====================================================
# System Health
# =====================================================

WATCHDOG_INTERVAL_SEC = 10
AUTO_RECOVERY_ENABLED = True

RESTART_ON_FAILURE = True

# =====================================================
# Strategy Control
# =====================================================

ALLOW_AUTO_STRATEGY_SWITCH = True
DISABLE_TRADING_ON_VOLATILITY = True

VOLATILITY_THRESHOLD = 0.02

# =====================================================
# Logging & Monitoring
# =====================================================

ENABLE_DETAILED_LOGGING = True
LOG_TRADE_HISTORY = True
LOG_RISK_EVENTS = True

# =====================================================
# Telegram Alerts
# =====================================================

ENABLE_TELEGRAM_ALERTS = True
ALERT_ON_ERROR = True
ALERT_ON_DRAWDOWN = True
ALERT_ON_ORDER_FAILURE = True

# =====================================================
# Environment
# =====================================================

ENV = "production"
DEBUG = False
