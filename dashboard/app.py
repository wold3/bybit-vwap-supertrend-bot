from flask import Flask, jsonify, render_template


from trade_db import trade_db


from position.position_manager import position_manager


from risk.drawdown_guard import drawdown_guard



app = Flask(__name__)




# ======================================
# HOME
# ======================================

@app.route("/")
def home():

    return render_template(
        "dashboard.html"
    )





# ======================================
# TRADES API
# ======================================

@app.route("/api/trades")
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





# ======================================
# POSITION API
# ======================================

@app.route("/api/positions")
def positions():


    return jsonify(

        position_manager.get_positions()

    )





# ======================================
# SUMMARY API
# ======================================

@app.route("/api/summary")
def summary():


    positions = (

        position_manager
        .get_positions()

    )


    unrealized_pnl = sum(

        float(
            p.get(
                "unrealized_pnl",
                0
            )
        )

        for p in positions

    )



    return jsonify({

        "positions":

            len(positions),


        "unrealized_pnl":

            unrealized_pnl,


        "risk":

            drawdown_guard.get_status()

    })





# ======================================
# EQUITY CURVE API
# ======================================

@app.route("/api/equity")
def equity():


    try:


        return jsonify(

            drawdown_guard.history

        )


    except Exception as e:


        print(
            "[EQUITY API ERROR]",
            e
        )


        return jsonify([])





# ======================================
# RISK API
# ======================================

@app.route("/api/risk")
def risk():


    try:


        return jsonify(

            drawdown_guard.get_status()

        )


    except Exception as e:


        return jsonify({

            "error":str(e)

        })





# ======================================
# HEALTH CHECK
# ======================================

@app.route("/api/health")
def health():


    return jsonify({

        "status":
        "RUNNING"

    })





# ======================================
# RUN
# ======================================

if __name__ == "__main__":


    print(
        "🚀 Dashboard running"
    )


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )
