# =====================================================
# web/server.py
# Dashboard Server
# Demo / Live Trading Mode Control
# =====================================================

from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

import threading


from config import (
    WEB_HOST,
    WEB_PORT
)





# =====================================================
# FLASK APP
# =====================================================

app = Flask(__name__)





# =====================================================
# THREAD LOCK
# =====================================================

lock = threading.Lock()





# =====================================================
# BOT STATUS
# =====================================================

status = {


    "bot":

        "STOPPED",


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









# =====================================================
# TRADING MODE
# =====================================================

mode = {


    "value":

        "DEMO"


}









# =====================================================
# LOG BUFFER
# =====================================================

logs = []









# =====================================================
# STATUS UPDATE
# =====================================================

def update_status(data):


    if not isinstance(data, dict):

        return



    with lock:


        status.update(

            data

        )









# =====================================================
# ADD LOG
# =====================================================

def add_log(message):


    with lock:


        logs.append(

            str(message)

        )



        if len(logs) > 300:


            logs.pop(0)









# =====================================================
# GET CURRENT MODE
# =====================================================

def get_trading_mode():


    with lock:


        return mode["value"]










# =====================================================
# CHANGE MODE
# =====================================================

def set_trading_mode(new_mode):


    new_mode = str(

        new_mode

    ).upper()





    if new_mode not in [

        "DEMO",

        "LIVE"

    ]:


        return False





    with lock:


        mode["value"] = new_mode





    add_log(

        f"MODE CHANGE : {new_mode}"

    )



    return True










# =====================================================
# DASHBOARD PAGE
# =====================================================

@app.route("/")

def dashboard():


    return render_template(

        "dashboard.html"

    )









# =====================================================
# STATUS API
# =====================================================

@app.route("/api/status")

def status_api():


    with lock:


        return jsonify({


            "status":

                status.copy(),



            "mode":

                mode["value"],



            "logs":

                logs.copy()


        })









# =====================================================
# MODE GET
# =====================================================

@app.route("/api/mode")

def mode_get():


    return jsonify({


        "mode":

            get_trading_mode()


    })









# =====================================================
# MODE CHANGE
# =====================================================

@app.route(
    "/api/mode",
    methods=["POST"]
)

def mode_change():


    data = request.get_json(

        silent=True

    ) or {}



    new_mode = data.get(

        "mode"

    )



    result = set_trading_mode(

        new_mode

    )



    return jsonify({


        "success":

            result,


        "mode":

            get_trading_mode()


    })









# =====================================================
# CHART API
# =====================================================

@app.route("/api/chart")

def chart_api():


    try:


        from web.chart_data import (

            get_chart

        )


        return jsonify(

            get_chart()

        )



    except Exception as e:


        add_log(

            f"CHART ERROR : {e}"

        )


        return jsonify([])









# =====================================================
# HEALTH CHECK
# =====================================================

@app.route("/api/health")

def health():


    return jsonify({


        "server":

            "OK",


        "mode":

            get_trading_mode()


    })









# =====================================================
# SERVER RUN
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
