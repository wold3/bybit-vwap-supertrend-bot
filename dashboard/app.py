from flask import Flask, jsonify, render_template

from trade_db import trade_db


app = Flask(__name__)



# ======================================
# DASHBOARD
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




if __name__ == "__main__":


    print(
        "🚀 Dashboard : http://localhost:5000"
    )


    app.run(

        host="0.0.0.0",

        port=5000

    )
