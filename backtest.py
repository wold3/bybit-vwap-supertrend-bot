import pandas as pd


INITIAL_BALANCE = 1000.0


def run_backtest(file):
    """
    CSV 백테스트

    Required Columns
    ----------------
    close
    signal
    """

    df = pd.read_csv(file)

    balance = INITIAL_BALANCE

    position = 0

    entry_price = 0.0

    wins = 0

    losses = 0

    trades = 0

    total_pnl = 0.0

    equity_curve = [balance]

    for _, row in df.iterrows():

        price = float(row["close"])

        signal = str(row["signal"]).upper()

        # -------------------------
        # BUY
        # -------------------------

        if signal == "BUY" and position == 0:

            position = 1

            entry_price = price

        # -------------------------
        # SELL
        # -------------------------

        elif signal == "SELL" and position == 1:

            pnl = price - entry_price

            balance += pnl

            total_pnl += pnl

            trades += 1

            if pnl >= 0:
                wins += 1
            else:
                losses += 1

            equity_curve.append(balance)

            position = 0

            entry_price = 0.0

    # 마지막 포지션 정리
    if position == 1:

        last_price = float(df.iloc[-1]["close"])

        pnl = last_price - entry_price

        balance += pnl

        total_pnl += pnl

        trades += 1

        if pnl >= 0:
            wins += 1
        else:
            losses += 1

        equity_curve.append(balance)

    # -------------------------
    # 통계 계산
    # -------------------------

    win_rate = (
        wins / trades * 100
        if trades
        else 0.0
    )

    roi = (
        (balance - INITIAL_BALANCE)
        / INITIAL_BALANCE
        * 100
    )

    peak = equity_curve[0]

    max_drawdown = 0.0

    for equity in equity_curve:

        if equity > peak:
            peak = equity

        drawdown = peak - equity

        if drawdown > max_drawdown:
            max_drawdown = drawdown

    return {

        "initial_balance": round(
            INITIAL_BALANCE,
            2,
        ),

        "final_balance": round(
            balance,
            2,
        ),

        "total_pnl": round(
            total_pnl,
            2,
        ),

        "roi": round(
            roi,
            2,
        ),

        "trades": trades,

        "wins": wins,

        "losses": losses,

        "win_rate": round(
            win_rate,
            2,
        ),

        "max_drawdown": round(
            max_drawdown,
            2,
        ),
    }
