import pandas as pd

INITIAL_BALANCE = 1000


def run_backtest(file):

    df = pd.read_csv(file)

    balance = INITIAL_BALANCE
    position = 0
    entry = 0
    wins = 0
    trades = 0

    for i in range(len(df)):

        price = df.iloc[i]["close"]
        signal = df.iloc[i]["signal"]

        if signal == "BUY" and position == 0:
            position = 1
            entry = price
            trades += 1

        elif signal == "SELL" and position == 1:
            pnl = price - entry
            balance += pnl

            if pnl > 0:
                wins += 1

            trades += 1
            position = 0

    win_rate = (wins / trades * 100) if trades else 0

    return {
        "balance": balance,
        "trades": trades,
        "win_rate": win_rate
    }


if __name__ == "__main__":
    print(run_backtest("data.csv"))
