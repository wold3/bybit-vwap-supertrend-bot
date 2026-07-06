from flask import Flask, jsonify
from storage.trade_db import trade_db
from execution.pnl_tracker import pnl_tracker

app = Flask(__name__)


@app.route("/trades")
def trades():
    return jsonify(trade_db.all())


@app.route("/pnl")
def pnl():
    return jsonify({
        "total_pnl": pnl_tracker.total_pnl()
    })


@app.route("/status")
def status():
    return jsonify({
        "status": "running"
    })


if __name__ == "__main__":
    app.run(port=5000)
