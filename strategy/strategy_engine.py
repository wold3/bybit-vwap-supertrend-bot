class StrategyEngine:

    def __init__(self, execution_engine):

        self.execution = execution_engine
        self.prices = []
        self.volumes = []

    # =================================================
    # WS PRICE INPUT
    # =================================================
    def on_price(self, price):

        self.prices.append(price)
        self.volumes.append(1)

        if len(self.prices) > 50:
            self.prices.pop(0)
            self.volumes.pop(0)

        # 충분한 데이터 없으면 skip
        if len(self.prices) < 20:
            return

        self.evaluate()

    # =================================================
    # STRATEGY RUN
    # =================================================
    def evaluate(self):

        from risk.risk_engine import risk_engine
        from ml_filter import ml_filter
        from indicators.vwap_supertrend import calculate_vwap, supertrend
        from portfolio.position_manager import position_manager

        symbol = "BTCUSDT"

        # 🚨 RISK GATE
        if not risk_engine.can_trade():
            return

        # 포지션 체크
        if position_manager.get_position(symbol):
            return

        vwap = calculate_vwap(self.prices, self.volumes)
        st = supertrend(self.prices)

        last_price = self.prices[-1]

        # TECH SIGNAL
        if last_price > vwap and st == "UP":
            base_signal = "BUY"
        elif last_price < vwap and st == "DOWN":
            base_signal = "SELL"
        else:
            return

        # ML FILTER
        allow, prob = ml_filter.allow_trade(self.prices, self.volumes)

        if not allow:
            return

        print(f"[WS STRATEGY] SIGNAL {base_signal} prob={prob:.2f}")

        # EXECUTE REAL TRADE
        self.execution.execute(
            symbol=symbol,
            side=base_signal,
            qty=0.001,
            price=last_price
        )
