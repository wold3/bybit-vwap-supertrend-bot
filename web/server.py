# =====================================================
# web/server.py
# Dashboard Web Server
# =====================================================

from flask import (
    Flask,
    jsonify,
    render_template
)

import threading
import time



from config import (
    WEB_HOST,
    WEB_PORT
)


from database.database import (
    database
)


from web.chart_data import (
    chart_data
)





app = Flask(
    __name__,
    template_folder="templates"
)





# =====================================================
# STATUS MEMORY
# =====================================================


status = {


    "bot":

        "STOPPED",


    "symbol":

        "BTCUSDT",


    "price":

        0,


    "vwap":

        0,


    "trend":

        "NONE",


    "volume":

        False,


    "signal":

        "NONE",


    "position":

        "NONE",


    "size":

        0,


    "entry":

        0,


    "pnl":

        0,


    "tp":

        0,


    "sl":

        0,


    "order":

        "",


    "stats":

        {}

}



logs = []






# =====================================================
# UPDATE STATUS
# =====================================================


def update_status(data):


    try:


        status.update(

            data

        )


    except Exception as e:


        print(

            "[STATUS ERROR]",

            e

        )









# =====================================================
# ADD LOG
# =====================================================


def add_log(message):


    try:


        text = (

            time.strftime(

                "%H:%M:%S"

            )

            +

            " "

            +

            str(message)

        )


        logs.append(

            text

        )



        if len(logs) > 200:


            del logs[0]



        database.save_log(

            text

        )



    except Exception as e:


        print(

            "[LOG ERROR]",

            e

        )









# =====================================================
# DASHBOARD
# =====================================================


@app.route("/")
def index():


    try:


        return render_template(

            "dashboard.html"

        )


    except:


        return """

        <h1>VWAP SUPERTREND BOT</h1>

        <p>Dashboard Running</p>

        """









# =====================================================
# STATUS API
# =====================================================


@app.route(
    "/api/status"
)

def api_status():


    status["stats"] = (

        database

        .get_trade_stats()

    )



    return jsonify({


        "status":

            status,


        "logs":

            logs[-50:]

    })









# =====================================================
# CHART API
# =====================================================


@app.route(
    "/api/chart"
)

def api_chart():


    return jsonify(

        chart_data.get()

    )









# =====================================================
# TRADES API
# =====================================================


@app.route(
    "/api/trades"
)

def api_trades():


    return jsonify(

        database

        .get_recent_trades()

    )









# =====================================================
# SERVER THREAD
# =====================================================


def run_server():


    app.run(

        host=

            WEB_HOST,


        port=

            WEB_PORT,


        debug=False,


        use_reloader=False

    )









def start_dashboard():


    thread = threading.Thread(

        target=run_server,

        daemon=True

    )


    thread.start()



    print(

        "[WEB SERVER START]",

        WEB_PORT

    )
