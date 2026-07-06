from datetime import datetime

from sqlalchemy import and_, desc, func, select

from database.models import (
    BotState,
    DailyStat,
    Position,
    Trade,
)
from database.session import get_session

# =====================================================
# Trade
# =====================================================


def add_trade(
    symbol: str,
    side: str,
    qty: float,
    price: float,
    strategy: str = "",
    regime: str = "",
    order_id: str = "",
    status: str = "OPEN",
    pnl: float = 0.0,
) -> Trade:

    trade = Trade(
        symbol=symbol,
        side=side,
        qty=qty,
        price=price,
        strategy=strategy,
        regime=regime,
        order_id=order_id,
        status=status,
        pnl=pnl,
    )

    with get_session() as db:

        db.add(trade)

        db.flush()

        db.refresh(trade)

        return trade


def get_trade(
    trade_id: int,
):

    with get_session() as db:

        return db.get(
            Trade,
            trade_id,
        )


def get_recent_trades(
    limit: int = 100,
):

    with get_session() as db:

        stmt = (
            select(Trade)
            .order_by(
                desc(
                    Trade.created_at
                )
            )
            .limit(limit)
        )

        return list(
            db.scalars(stmt)
        )


def get_open_trades():

    with get_session() as db:

        stmt = (
            select(Trade)
            .where(
                Trade.status == "OPEN"
            )
            .order_by(
                desc(
                    Trade.created_at
                )
            )
        )

        return list(
            db.scalars(stmt)
        )


def update_trade_pnl(
    trade_id: int,
    pnl: float,
    status: str = "CLOSED",
):

    with get_session() as db:

        trade = db.get(
            Trade,
            trade_id,
        )

        if trade is None:
            return None

        trade.pnl = pnl

        trade.status = status

        db.add(trade)

        return trade


def close_trade(
    trade_id: int,
    pnl: float,
):

    return update_trade_pnl(
        trade_id,
        pnl,
        "CLOSED",
    )


# =====================================================
# Position
# =====================================================


def save_position(
    symbol: str,
    side: str,
    qty: float,
    entry_price: float,
    leverage: int,
):

    with get_session() as db:

        stmt = (
            select(Position)
            .where(
                Position.symbol == symbol
            )
        )

        position = db.scalar(stmt)

        if position is None:

            position = Position(
                symbol=symbol,
                side=side,
                qty=qty,
                entry_price=entry_price,
                leverage=leverage,
            )

        else:

            position.side = side

            position.qty = qty

            position.entry_price = entry_price

            position.leverage = leverage

            position.updated_at = (
                datetime.utcnow()
            )

        db.add(position)

        return position


def update_position_price(
    symbol: str,
    mark_price: float,
    unrealized_pnl: float,
):

    with get_session() as db:

        stmt = (
            select(Position)
            .where(
                Position.symbol == symbol
            )
        )

        position = db.scalar(stmt)

        if position is None:
            return None

        position.mark_price = mark_price

        position.unrealized_pnl = unrealized_pnl

        position.updated_at = (
            datetime.utcnow()
        )

        db.add(position)

        return position


def get_position(
    symbol: str,
):

    with get_session() as db:

        stmt = (
            select(Position)
            .where(
                Position.symbol == symbol
            )
        )

        return db.scalar(stmt)


def get_positions():

    with get_session() as db:

        stmt = select(Position)

        return list(
            db.scalars(stmt)
        )


def has_position(
    symbol: str,
):

    with get_session() as db:

        stmt = (
            select(Position)
            .where(
                Position.symbol == symbol
            )
        )

        return db.scalar(stmt) is not None

def delete_position(
    symbol: str,
):

    with get_session() as db:

        stmt = (
            select(Position)
            .where(
                Position.symbol == symbol
            )
        )

        position = db.scalar(stmt)

        if position is None:
            return False

        db.delete(position)

        return True


# =====================================================
# Daily Statistics
# =====================================================

def get_or_create_daily_stat(
    date: str,
):

    with get_session() as db:

        stmt = (
            select(DailyStat)
            .where(
                DailyStat.date == date
            )
        )

        stat = db.scalar(stmt)

        if stat is None:

            stat = DailyStat(
                date=date,
            )

            db.add(stat)

            db.flush()

            db.refresh(stat)

        return stat


def update_daily_stat(
    date: str,
    pnl: float,
    win: bool,
):

    with get_session() as db:

        stmt = (
            select(DailyStat)
            .where(
                DailyStat.date == date
            )
        )

        stat = db.scalar(stmt)

        if stat is None:

            stat = DailyStat(
                date=date,
            )

        stat.trades += 1

        stat.pnl += pnl

        if win:
            stat.wins += 1
        else:
            stat.losses += 1

        db.add(stat)

        return stat


def get_today_pnl(
    date: str,
):

    with get_session() as db:

        stmt = (
            select(DailyStat)
            .where(
                DailyStat.date == date
            )
        )

        stat = db.scalar(stmt)

        if stat is None:
            return 0.0

        return stat.pnl


# =====================================================
# Bot State
# =====================================================

def update_bot_state(
    running: bool,
    signal: str,
    price: float,
):

    with get_session() as db:

        state = db.get(
            BotState,
            1,
        )

        if state is None:

            state = BotState(
                id=1,
            )

        state.running = running
        state.last_signal = signal
        state.last_price = price
        state.updated_at = datetime.utcnow()

        db.add(state)

        return state


def get_bot_state():

    with get_session() as db:

        return db.get(
            BotState,
            1,
        )


# =====================================================
# Statistics
# =====================================================

def get_trade_count():

    with get_session() as db:

        return db.scalar(
            select(func.count())
            .select_from(Trade)
        )


def get_total_pnl():

    with get_session() as db:

        return (
            db.scalar(
                select(
                    func.sum(
                        Trade.pnl
                    )
                )
            )
            or 0.0
        )


def get_win_rate():

    with get_session() as db:

        total = db.scalar(
            select(func.count())
            .select_from(Trade)
        )

        if not total:
            return 0.0

        wins = db.scalar(
            select(func.count())
            .select_from(Trade)
            .where(
                Trade.pnl > 0
            )
        )

        return round(
            wins / total * 100,
            2,
        )


def get_open_position_count():

    with get_session() as db:

        return db.scalar(
            select(func.count())
            .select_from(Position)
        )


# =====================================================
# Dashboard Summary
# =====================================================

def get_summary():

    with get_session() as db:

        trade_count = get_trade_count()

        total_pnl = get_total_pnl()

        open_positions = get_open_position_count()

        wins = db.scalar(
            select(func.count())
            .select_from(Trade)
            .where(
                Trade.pnl > 0
            )
        )

        losses = db.scalar(
            select(func.count())
            .select_from(Trade)
            .where(
                Trade.pnl < 0
            )
        )

        return {

            "trade_count": trade_count,

            "open_positions": open_positions,

            "total_pnl": round(
                total_pnl,
                2,
            ),

            "wins": wins,

            "losses": losses,

            "win_rate": get_win_rate(),
        }
