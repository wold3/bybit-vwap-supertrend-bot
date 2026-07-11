# =====================================================
# web/server.py
# Flask Dashboard Server
# =====================================================

from flask import (
    Flask,
    jsonify,
    request,
    render_template
)

import threading



app = Flask(
    __name__,
    template_folder="templates"
)





# =====================================================
# GLOBAL STATUS
# =====================================================

STATUS = {


    "bot":

        "STOPPED",


    "mode":

        "DEMO",


    "position":

        "NONE",


    "position_size":

        0,


    "entry_price":

        0,


    "pnl":

        0,


    "signal":

        "WAIT",


    "watchdog":

        "OFF"


}





LOGS = []



CURRENT_MODE = "DEMO"









# =====================================================
# STATUS UPDATE
# =====================================================

def update_status(data):


    STATUS.update(

        data

    )









# =====================================================
# LOG
# =====================================================

def add_log(message):


    LOGS.append(

        str(message)

    )


    if len(LOGS) > 100:


        LOGS.pop(0)









# =====================================================
# MODE
# =====================================================

def get_trading_mode():


    return CURRENT_MODE







# =====================================================
# CHANGE MODE
# =====================================================

def change_mode(mode):


    global CURRENT_MODE



    mode = mode.upper()



    if mode not in [

        "DEMO",

        "LIVE"

    ]:


        return False





    CURRENT_MODE = mode



    STATUS["mode"] = mode



    add_log(

        f"MODE CHANGE : {mode}"

    )



    return True







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

def status():


    return jsonify({

        "status":

            STATUS,

        "logs":

            LOGS[-30:]

    })









# =====================================================
# MODE API
# =====================================================

@app.route(

    "/api/mode",

    methods=["POST"]

)

def mode():


    data = request.json



    new_mode = data.get(

        "mode",

        ""

    )



    result = change_mode(

        new_mode

    )



    return jsonify({

        "success":

            result,


        "mode":

            CURRENT_MODE

    })









# =====================================================
# SERVER START
# =====================================================

def start_server():


    print(

        "[WEB SERVER START] 8000"

    )


    app.run(

        host="0.0.0.0",

        port=8000,

        debug=False,

        use_reloader=False

    )









def run_server():


    thread = threading.Thread(

        target=start_server,

        daemon=True

    )


    thread.start()
