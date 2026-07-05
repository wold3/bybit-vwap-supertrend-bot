from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute
from state import get_position, can_trade, update_price, update_trailing, should_exit, positions
from telegram import send_message

from market_regime import get_market_regime
from portfolio_engine import portfolio
from strategy_wrapper import execute_strategy

from ai_filter import allow_trade
from feature_engine import get_features
from ml_filter import should_enter_market
from position_sizer import calculate_qty

from risk_engine import should_stop_trading, update_pnl

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    if should_stop_trading():
        return jsonify({"blocked": "risk_engine"}), 403

    data = request.get_json(force=True, silent=True)

    ok, result = validate(data)

    if not ok:
        return jsonify({"error": result}), 400

    symbol = result["symbol"]
    price = float(data.get("price", 0))
    signal = result["signal"]

    pos = get_position(symbol)

    regime = get_market_regime()
    strategy = portfolio.allocate(regime)

    allowed = execute_strategy(strategy, signal)

    if not allowed:
        return jsonify({"blocked": "strategy"}), 403

    ok_ai, _ = allow_trade()
    if not ok_ai:
        return jsonify({"blocked": "ai_filter"}), 403

    features = get_features(symbol, price)

    ok_ml, score = should_enter_market(
        price,
        features["volatility"],
        features["trend_strength"]
    )

    if not ok_ml:
        return jsonify({"blocked": "ml_filter", "score": score}), 403

    update_price(symbol, price)
    update_trailing(symbol)

    if should_exit(symbol, price):
        execute("EXIT", symbol, result["qty"])
        update_pnl(-1)
        pos["active"] = False
        return jsonify({"exit": True})

    if not can_trade():
        return jsonify({"error": "rate_limit"}), 429

    if signal == "BUY":

        stop_loss = price * 0.99
        qty = calculate_qty(price, stop_loss)

        pos["active"] = True
        pos["entry_price"] = price
        pos["highest_price"] = price
        pos["trailing_stop"] = stop_loss

        execute("BUY", symbol, qty)

        send_message(
            f"📈 ENTRY {symbol}\n"
            f"Price: {price}\n"
            f"Qty: {qty}\n"
            f"Strategy: {strategy}\n"
            f"ML: {score}"
        )

    return jsonify({"ok": True})


@app.route("/pnl")
def pnl():
    return jsonify(positions)


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
