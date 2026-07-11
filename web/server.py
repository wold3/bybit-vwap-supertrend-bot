# =====================================================
# web/server.py
# VWAP SUPERTREND AUTO BOT DASHBOARD
# =====================================================


from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

import os
import time
import threading



from config import (
    WEB_HOST,
    WEB_PORT
)



# =====================================================
# TEMPLATE PATH
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


TEMPLATE_DIR = os.path.join(
    BASE_DIR,
    "templates"
)



app = Flask(

    __name__,

    template_folder=TEMPLATE_DIR

)





# =====================================================
# GLOBAL
# =====================================================


bot_instance = None


server_started = False


server_thread = None



MAX_LOGS = 500



status_lock = threading.Lock()

log_lock = threading.Lock()



status = {


    "mode":
        "DEMO",


    "bot":
        "STOPPED",


    "position":
        "NONE",


    "position_size":
        0,


    "entry_price":
        0,


    "pnl":
        0,


    "price":
        0,


    "balance":
        0,


    "signal":
        "NONE"

}




logs = []







# =====================================================
# LOG
# =====================================================

def add_log(message):


    text = (

        "["

        + time.strftime("%H:%M:%S")

        + "] "

        + str(message)

    )


    print(text)



    with log_lock:


        logs.append(text)


        if len(logs) > MAX_LOGS:


            logs.pop(0)







# =====================================================
# STATUS
# =====================================================

def update_status(data):


    if not data:

        return



    with status_lock:


        status.update(data)







def get_status():


    with status_lock:


        return status.copy()







# =====================================================
# BOT INSTANCE
# =====================================================

def set_bot_instance(bot):


    global bot_instance


    bot_instance = bot


    add_log(

        "BOT INSTANCE CONNECTED"

    )








# =====================================================
# MODE
# =====================================================

def get_trading_mode():


    with status_lock:


        return status["mode"]







# =====================================================
# HOME
# =====================================================

@app.route("/")

def index():


    return render_template(

        "index.html"

    )







# =====================================================
# STATUS API
# =====================================================

@app.route("/api/status")

def api_status():


    with log_lock:


        log_copy = logs[-200:]



    return jsonify({


        "status":

            get_status(),


        "logs":

            log_copy


    })









# =====================================================
# START
# =====================================================

@app.route(

    "/api/start",

    methods=["POST"]

)

def api_start():


    add_log(

        "BUTTON CLICK : START"

    )


    try:


        if bot_instance:


            bot_instance.start()



        update_status({

            "bot":

                "RUNNING"

        })


        add_log(

            "BOT START COMPLETE"

        )



        return jsonify({

            "success":

                True

        })



    except Exception as e:


        add_log(

            f"START ERROR {e}"

        )


        return jsonify({

            "success":

                False

        })










# =====================================================
# STOP
# =====================================================

@app.route(

    "/api/stop",

    methods=["POST"]

)

def api_stop():


    add_log(

        "BUTTON CLICK : STOP"

    )


    try:


        if bot_instance:


            bot_instance.stop()



        update_status({

            "bot":

                "STOPPED"

        })


        add_log(

            "BOT STOP COMPLETE"

        )



        return jsonify({

            "success":

                True

        })



    except Exception as e:


        add_log(

            f"STOP ERROR {e}"

        )


        return jsonify({

            "success":

                False

        })









# =====================================================
# MODE
# =====================================================

@app.route(

    "/api/mode",

    methods=["POST"]

)

def api_mode():


    data = request.get_json(

        silent=True

    ) or {}



    mode = data.get(

        "mode",

        "DEMO"

    ).upper()



    add_log(

        f"BUTTON CLICK : MODE {mode}"

    )



    if mode not in (

        "DEMO",

        "LIVE"

    ):


        return jsonify({

            "success":

                False

        })



    update_status({

        "mode":

            mode

    })



    try:


        from api.bybit_api import bybit_api


        bybit_api.change_session(

            mode

        )


        add_log(

            f"MODE CHANGED {mode}"

        )



    except Exception as e:


        add_log(

            f"MODE ERROR {e}"

        )



    return jsonify({

        "success":

            True,

        "mode":

            mode

    })









# =====================================================
# CLOSE POSITION
# =====================================================

@app.route(

    "/api/close",

    methods=["POST"]

)

def api_close():


    add_log(

        "BUTTON CLICK : CLOSE POSITION"

    )



    try:


        from order.order_manager import order_manager



        result = order_manager.close_position()



        if result:


            add_log(

                "POSITION CLOSED"

            )



        else:


            add_log(

                "CLOSE FAILED"

            )



        return jsonify({

            "success":

                bool(result)

        })



    except Exception as e:


        add_log(

            f"CLOSE ERROR {e}"

        )


        return jsonify({

            "success":

                False

        })








# =====================================================
# RESET
# =====================================================

@app.route(

    "/api/reset",

    methods=["POST"]

)

def api_reset():


    add_log(

        "BUTTON CLICK : RESET"

    )


    update_status({

        "position":

            "NONE",

        "position_size":

            0,

        "entry_price":

            0,

        "pnl":

            0

    })



    return jsonify({

        "success":

            True

    })







# =====================================================
# BOT INSTANCE
# =====================================================

def run_server():


    global server_started

    global server_thread



    if server_started:

        return



    server_started = True



    def run():


        app.run(

            host=WEB_HOST,

            port=WEB_PORT,

            debug=False,

            use_reloader=False,

            threaded=True

        )





    server_thread = threading.Thread(

        target=run,

        daemon=True,

        name="WebServer"

    )



    server_thread.start()



    print(

        "[WEB SERVER READY]"

    )


    add_log(

        "WEB SERVER READY"

    )







# =====================================================
# EXPORT
# =====================================================

__all__ = [


    "app",

    "run_server",

    "set_bot_instance",

    "update_status",

    "get_status",

    "add_log",

    "get_trading_mode"

]
