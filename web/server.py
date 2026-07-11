# =====================================================
# web/server.py
# Flask Dashboard Server
# =====================================================

from flask import (
    Flask,
    render_template,
    jsonify
)


import threading





from config import (
    WEB_HOST,
    WEB_PORT
)





app = Flask(

    __name__

)





# =====================================================
# GLOBAL STATUS
# =====================================================


status = {


    "bot":

        "STARTING",


    "price":

        0,


    "vwap":

        0,


    "trend":

        "-",


    "signal":

        "-",


    "position":

        "NONE",


    "entry":

        0,


    "size":

        0,


    "pnl":

        0,


    "watchdog":

        "OFF"


}





logs = []



lock = threading.Lock()







# =====================================================
# UPDATE STATUS
# =====================================================


def update_status(
    data
):


    with lock:


        status.update(

            data

        )









# =====================================================
# LOG
# =====================================================


def add_log(
    message
):


    with lock:


        logs.append(

            message

        )



        if len(logs) > 100:


            logs.pop(0)









# =====================================================
# PAGE
# =====================================================


@app.route("/")

def index():


    return render_template(

        "dashboard.html"

    )









# =====================================================
# STATUS API
# =====================================================


@app.route("/api/status")

def api_status():


    with lock:


        return jsonify({


            "status":

                status.copy(),


            "logs":

                logs.copy()

        })









# =====================================================
# CHART API
# =====================================================


@app.route("/api/chart")

def api_chart():


    try:


        from web.chart_data import (

            get_chart

        )


        return jsonify(

            get_chart()

        )



    except Exception:


        return jsonify(

            []

        )









# =====================================================
# SERVER START
# =====================================================


def run_server():


    print(

        "[WEB SERVER START]",

        WEB_PORT

    )


    app.run(

        host=

        WEB_HOST,


        port=

        WEB_PORT,


        debug=False,


        use_reloader=False

    )
