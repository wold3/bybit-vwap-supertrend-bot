from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute
from state import get_position, can_trade, update_price, update_trailing, should_exit, positions
from telegram import send_message

from strategy_router import route
from ai_filter import allow_trade
from feature_engine import get_features
from ml_filter import should_enter_market
from position_sizer import calculate_qty

from risk_engine import should_stop_trading, update_pnl
from config import USE_AI_FILTER

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

    # 전략
    features = get_features(symbol, price)
    allowed, regime = route(signal, features["price_action"])

    if not allowed:
        return jsonify({"blocked": regime}), 403

    # AI
    if USE_AI_FILTER:
        ok_ai, _ = allow_trade()
        if not ok_ai:
            return jsonify({"blocked": "ai_filter"}), 403

    # ML
    ok_ml, score = should_enter_market(
        price,
        features["volatility"],
        features["trend_strength"]
    )

    if not ok_ml:
        return jsonify({"blocked": "ml_filter", "score": score}), 403

    # 트레일링
    update_price(symbol, price)
    update_trailing(symbol)

    # EXIT
    if should_exit(symbol, price):
        execute("EXIT", symbol, result["qty"])
        update_pnl(-1)
        pos["active"] = False
        return jsonify({"exit": True})

    # 거래 제한
    if not can_trade():
        return jsonify({"error": "rate_limit"}), 429

    # ENTRY
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
            f"Regime: {regime}\n"
            f"ML Score: {score}"
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
