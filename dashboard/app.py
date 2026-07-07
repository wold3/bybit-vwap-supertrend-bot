from flask import Flask, jsonify, render_template


from position.position_manager import position_manager


from execution.execution_engine import execution_engine


from risk.drawdown_guard import drawdown_guard


from trade_db import trade_db



import time



app = Flask(
    __name__,
    template_folder="templates"
)





# =====================================
# DASHBOARD PAGE
# =====================================

@app.route("/")
def dashboard():


    return render_template(

        "dashboard.html"

    )





# =====================================
# SUMMARY
# =====================================

@app.route(
    "/api/summary"
)

def summary():


    positions = (

        position_manager
        .get_positions()

    )



    pnl = sum(

        [

            p.get(
                "unrealized_pnl",
                0
            )

            for p in positions

        ]

    )



    return jsonify({


        "positions":

            len(positions),


        "unrealized_pnl":

            pnl


    })





# =====================================
# POSITIONS
# =====================================

@app.route(
    "/api/positions"
)

def positions():


    return jsonify(

        position_manager
        .get_positions()

    )





# =====================================
# EQUITY CURVE
# =====================================

@app.route(
    "/api/equity"
)

def equity():


    history = (

        drawdown_guard
        .get_history()

    )


    return jsonify(

        history

    )





# =====================================
# RISK
# =====================================

@app.route(
    "/api/risk"
)

def risk():


    data = (

        drawdown_guard
        .status()

    )


    return jsonify(

        data

    )





# =====================================
# TRADES
# =====================================

@app.route(
    "/api/trades"
)

def trades():


    data = (

        trade_db
        .get_recent()

    )


    return jsonify(

        data

    )





# =====================================
# BOT STATUS
# =====================================

@app.route(
    "/api/status"
)

def status():


    return jsonify({


        "status":

            "RUNNING",


        "time":

            time.time()


    })





# =====================================
# MANUAL CLOSE
# =====================================

@app.route(
    "/api/close/<symbol>"
)

def close(symbol):


    position = (

        position_manager
        .get_position(

            symbol

        )

    )


    if not position:


        return jsonify({

            "error":

                "NO POSITION"

        })



    result = execution_engine.close_position(

        symbol,

        position["side"],

        position["size"]

    )



    return jsonify(

        result

    )





if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000

    )
