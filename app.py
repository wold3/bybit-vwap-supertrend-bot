from flask import Flask, request, jsonify

from signal_parser import validate
from bybit_api import execute
from state import get_position, can_trade, update_price, update_trailing, should_exit, positions
from telegram import send_message

from strategy_router import should_trade
from market_regime import get_market_regime
from ai_filter import allow_trade

from feature_engine import get_features
from ml_filter import should_enter_market
from position_sizer import calculate_qty
from config import USE_AI_FILTER, MAX_DAILY_LOSS

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True, silent=True)

    ok, result = validate(data)

    if not ok:
        return jsonify({"error": result}), 400

    symbol = result["symbol"]
    price = float(data.get("price", 0))
    signal = result["signal"]

    pos = get_position(symbol)

    # 시장 상태
    regime = get_market_regime()

    allowed, regime_name = should_trade(signal)

    if not allowed:
        return jsonify({"blocked": regime_name, "regime": regime}), 403

    # AI 필터
    if USE_AI_FILTER:
        ok_ai, reason = allow_trade()
        if not ok_ai:
            return jsonify({"blocked": reason}), 403

    # ML 필터
    features = get_features(symbol, price)

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
        send_message(f"🚨 EXIT {symbol} @ {price}")
        pos["active"] = False
        return jsonify({"exit": True})

    # 손실 제한
    if pos["daily_pnl"] <= MAX_DAILY_LOSS:
        return jsonify({"error": "loss limit"}), 403

    # 거래 제한
    if not can_trade():
        return jsonify({"error": "limit"}), 429

    # 진입
    if signal == "BUY":

        stop_loss = price * 0.99
        qty = calculate_qty(price, stop_loss)

        pos["active"] = True
        pos["entry_price"] = price
        pos["highest_price"] = price
        pos["stop_loss"] = stop_loss
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
