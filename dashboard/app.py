from flask import Flask, jsonify, render_template


from trade_db import trade_db


from position.position_manager import position_manager



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
# TRADES
# ======================================

@app.route("/api/trades")
def trades():


    rows = trade_db.all()



    return jsonify([


        {

            "id":r[0],

            "symbol":r[1],

            "side":r[2],

            "qty":r[3],

            "price":r[4],

            "pnl":r[5],

            "time":r[6]

        }


        for r in rows


    ])






# ======================================
# POSITIONS
# ======================================

@app.route("/api/positions")
def positions():


    return jsonify(

        position_manager.get_positions()

    )





# ======================================
# SUMMARY
# ======================================

@app.route("/api/summary")
def summary():


    positions = (

        position_manager
        .get_positions()

    )


    total_pnl = sum(

        p.get(
            "unrealized_pnl",
            0
        )

        for p in positions

    )


    return jsonify({

        "positions":

            len(positions),


        "unrealized_pnl":

            total_pnl


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
