from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database.database import Base


# =====================================================
# TRADE TABLE
# =====================================================

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String, index=True)
    side = Column(String)  # BUY / SELL

    qty = Column(Float)
    price = Column(Float)

    leverage = Column(Integer, default=1)

    pnl = Column(Float, default=0.0)

    status = Column(String, default="OPEN")  # OPEN / CLOSED

    created_at = Column(DateTime, default=datetime.utcnow)


# =====================================================
# PNL HISTORY
# =====================================================

class PnL(Base):
    __tablename__ = "pnl_history"

    id = Column(Integer, primary_key=True, index=True)

    trade_id = Column(Integer)

    pnl = Column(Float)

    balance = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)


# =====================================================
# SYSTEM LOGS
# =====================================================

class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)

    level = Column(String)  # INFO / ERROR / WARNING

    message = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
