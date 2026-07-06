from sqlalchemy.orm import Session

from database.models import Trade, PnL, SystemLog


# =====================================================
# TRADE
# =====================================================

def add_trade(db: Session, symbol, side, qty, price, leverage=1):

    trade = Trade(
        symbol=symbol,
        side=side,
        qty=qty,
        price=price,
        leverage=leverage,
        status="OPEN"
    )

    db.add(trade)
    db.commit()
    db.refresh(trade)

    return trade


def close_trade(db: Session, trade_id, pnl):

    trade = db.query(Trade).filter(Trade.id == trade_id).first()

    if not trade:
        return None

    trade.pnl = pnl
    trade.status = "CLOSED"

    db.commit()
    return trade


def get_open_trades(db: Session):

    return db.query(Trade).filter(Trade.status == "OPEN").all()


# =====================================================
# PNL
# =====================================================

def add_pnl(db: Session, trade_id, pnl, balance):

    record = PnL(
        trade_id=trade_id,
        pnl=pnl,
        balance=balance
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


# =====================================================
# SYSTEM LOG
# =====================================================

def add_log(db: Session, level, message):

    log = SystemLog(
        level=level,
        message=message
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log
