from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
)

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


# =====================================================
# Base
# =====================================================

class Base(DeclarativeBase):
    pass


# =====================================================
# Trade History
# =====================================================

class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    symbol: Mapped[str] = mapped_column(
        String(30),
        index=True,
    )

    side: Mapped[str] = mapped_column(
        String(10),
    )

    qty: Mapped[float] = mapped_column(
        Float,
    )

    price: Mapped[float] = mapped_column(
        Float,
    )

    pnl: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    strategy: Mapped[str] = mapped_column(
        String(50),
        default="",
    )

    regime: Mapped[str] = mapped_column(
        String(30),
        default="",
    )

    order_id: Mapped[str] = mapped_column(
        String(100),
        default="",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


# =====================================================
# Position
# =====================================================

class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    symbol: Mapped[str] = mapped_column(
        String(30),
        unique=True,
    )

    side: Mapped[str] = mapped_column(
        String(10),
    )

    qty: Mapped[float] = mapped_column(
        Float,
    )

    entry_price: Mapped[float] = mapped_column(
        Float,
    )

    mark_price: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    unrealized_pnl: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    leverage: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


# =====================================================
# Daily Statistics
# =====================================================

class DailyStat(Base):
    __tablename__ = "daily_stats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    date: Mapped[str] = mapped_column(
        String(20),
        unique=True,
    )

    trades: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    wins: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    losses: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    pnl: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    max_drawdown: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )


# =====================================================
# Bot State
# =====================================================

class BotState(Base):
    __tablename__ = "bot_state"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    running: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    last_signal: Mapped[str] = mapped_column(
        String(20),
        default="",
    )

    last_price: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
