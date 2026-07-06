from flask import Flask, jsonify
import time

from database.repository import trade_db


app = Flask(__name__)


# ================================
# HOME (PnL CHART UI)
# ================================
@app.route("/")
def home():

    return """
    <h1>🚀 REAL-TIME PnL CHART</h1>

    <canvas id="chart" width="900" height="400"></canvas>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <script>

        async function loadData() {

            const res = await fetch('/pnl-history');
            const data = await res.json();

            const labels = data.map(x =>
                new Date(x.time * 1000).toLocaleTimeString()
            );

            const values = data.map(x => x.pnl);

            const ctx = document.getElementById('chart');

            if (window.myChart) {
                window.myChart.destroy();
            }

            window.myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'PnL',
                        data: values,
                        borderColor: 'green',
                        fill: false,
                        tension: 0.2
                    }]
                },
                options: {
                    animation: false,
                    responsive: true
                }
            });
        }

        loadData();
        setInterval(loadData, 3000);

    </script>
    """


# ================================
# STATUS
# ================================
@app.route("/status")
def status():

    return jsonify({
        "status": "RUNNING",
        "time": time.time()
    })


# ================================
# TRADES
# ================================
@app.route("/trades")
def trades():

    rows = trade_db.all()

    return jsonify([
        {
            "id": r[0],
            "symbol": r[1],
            "side": r[2],
            "qty": r[3],
            "price": r[4],
            "pnl": r[5],
            "time": r[6]
        }
        for r in rows
    ])


# ================================
# PnL HISTORY API
# ================================
@app.route("/pnl-history")
def pnl_history():

    rows = trade_db.get_pnl_history()

    return jsonify([
        {
            "pnl": r[0],
            "time": r[1]
        }
        for r in rows
    ])


# ================================
# RUN SERVER
# ================================
if __name__ == "__main__":

    print("🚀 Dashboard running at http://localhost:5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
