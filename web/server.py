# =====================================================
# web/server.py
# VWAP SUPERTREND BOT DASHBOARD SERVER
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
# FLASK
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


app = Flask(

    __name__,

    template_folder=os.path.join(
        BASE_DIR,
        "templates"
    )

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



selected_symbol = "BTCUSDT"



status = {


    "mode":
        "DEMO",


    "symbol":
        "BTCUSDT",


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
# SYMBOL
# =====================================================

def get_trading_symbol():


    global selected_symbol


    return selected_symbol







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
# SYMBOL CHANGE
# =====================================================

@app.route(

    "/api/symbol",

    methods=["POST"]

)

def api_symbol():


    global selected_symbol



    data = request.get_json(

        silent=True

    ) or {}



    symbol = data.get(

        "symbol",

        "BTCUSDT"

    ).upper()



    symbols = [

        "BTCUSDT",

        "ETHUSDT",

        "SOLUSDT",

        "XRPUSDT",

        "DOGEUSDT"

    ]



    if symbol not in symbols:


        return jsonify({

            "success":
                False,

            "error":
                "INVALID SYMBOL"

        })





    # 포지션 보호

    pos = get_status().get(

        "position",

        "NONE"

    )


    size = get_status().get(

        "position_size",

        0

    )



    if size > 0:


        add_log(

            "SYMBOL CHANGE BLOCKED : POSITION EXISTS"

        )


        return jsonify({

            "success":
                False,

            "error":
                "POSITION EXISTS"

        })






    selected_symbol = symbol



    update_status({

        "symbol":
            symbol

    })



    add_log(

        f"SYMBOL CHANGE : {symbol}"

    )



    return jsonify({

        "success":
            True,

        "symbol":
            symbol

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

        "BUTTON : START"

    )


    try:


        if bot_instance:

            bot_instance.start()



        update_status({

            "bot":
                "RUNNING"

        })


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

        "BUTTON : STOP"

    )


    try:


        if bot_instance:

            bot_instance.stop()



        update_status({

            "bot":
                "STOPPED"

        })


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


    data=request.get_json(

        silent=True

    ) or {}



    mode=data.get(

        "mode",

        "DEMO"

    ).upper()



    if mode not in [

        "DEMO",

        "LIVE"

    ]:

        return jsonify({

            "success":
                False

        })




    update_status({

        "mode":
            mode

    })


    add_log(

        f"MODE CHANGE : {mode}"

    )



    try:


        from api.bybit_api import bybit_api


        bybit_api.change_session(

            mode

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
# CLOSE
# =====================================================

@app.route(

    "/api/close",

    methods=["POST"]

)

def api_close():


    add_log(

        "BUTTON : CLOSE"

    )


    try:


        from order.order_manager import order_manager



        result = order_manager.close_position()



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
# SERVER START
# =====================================================

def run_server():


    global server_started

    global server_thread



    if server_started:

        return



    server_started=True



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

        daemon=True

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

__all__=[


    "app",

    "run_server",

    "set_bot_instance",

    "update_status",

    "get_status",

    "add_log",

    "get_trading_mode",

    "get_trading_symbol"

]
