# =====================================================
# web/server.py
# VWAP SUPERTREND BOT WEB SERVER
# =====================================================

from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

import threading
import time


from config import (
    WEB_HOST,
    WEB_PORT,
    SYMBOL
)



app = Flask(
    __name__,
    template_folder="templates"
)



# =====================================================
# GLOBAL
# =====================================================

bot_instance = None


server_started = False


_server_thread = None



MAX_LOGS = 500



status_lock = threading.Lock()

log_lock = threading.Lock()

chart_lock = threading.Lock()





status = {


    "mode":
        "DEMO",


    "symbol":
        SYMBOL,


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


    "equity":
        0,


    "vwap":
        0,


    "trend":
        "NONE",


    "volume":
        0,


    "signal":
        "NONE",


    "watchdog":
        "OFF"

}





logs = []


chart_data = []





# =====================================================
# LOG
# =====================================================

def add_log(message):


    text = (

        f"[{time.strftime('%H:%M:%S')}] "

        f"{message}"

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
# MODE / SYMBOL
# =====================================================

def get_trading_mode():


    with status_lock:


        return status["mode"]






def get_trading_symbol():


    with status_lock:


        return status["symbol"]






# =====================================================
# BOT
# =====================================================

def set_bot_instance(bot):


    global bot_instance


    bot_instance = bot


    add_log(
        "BOT INSTANCE CONNECTED"
    )







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


        log_copy = logs[-100:]



    return jsonify({


        "status":
            get_status(),


        "logs":
            log_copy


    })






# =====================================================
# LOG
# =====================================================

@app.route("/api/logs")

def api_logs():


    with log_lock:


        return jsonify({

            "logs":
                logs.copy()

        })







# =====================================================
# SYMBOL
# =====================================================

@app.route(
    "/api/symbol",
    methods=["POST"]
)

def api_symbol():


    data = request.get_json(
        silent=True
    ) or {}



    symbol = data.get(
        "symbol",
        ""
    ).upper()



    if not symbol:


        return jsonify({

            "success":
                False

        })




    try:


        from api.bybit_api import bybit_api


        bybit_api.change_symbol(

            symbol

        )



        update_status({

            "symbol":
                symbol

        })



        add_log(

            f"SYMBOL CHANGE {symbol}"

        )



        return jsonify({

            "success":
                True,

            "symbol":
                symbol

        })



    except Exception as e:


        add_log(

            f"SYMBOL ERROR {e}"

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



    add_log(

        f"MODE CHANGE {mode}"

    )



    try:


        from api.bybit_api import bybit_api


        bybit_api.create_session()



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
# START
# =====================================================

@app.route(
    "/api/start",
    methods=["POST"]
)

def api_start():


    try:


        if bot_instance is None:


            return jsonify({

                "success":
                    False,

                "error":
                    "BOT NOT READY"

            })




        bot_instance.start()



        update_status({

            "bot":
                "RUNNING"

        })



        add_log(

            "BOT START"

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


    try:


        if bot_instance:


            bot_instance.stop()



        update_status({

            "bot":
                "STOPPED"

        })



        add_log(

            "BOT STOP"

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
# CLOSE
# =====================================================

@app.route(
    "/api/close",
    methods=["POST"]
)

def api_close():


    try:


        from order.order_manager import order_manager



        result = order_manager.close_position()



        add_log(

            "MANUAL CLOSE"

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
# CHART
# =====================================================

@app.route("/api/chart")

def api_chart():


    with chart_lock:


        return jsonify(

            chart_data.copy()

        )





def update_chart(data):


    with chart_lock:


        chart_data.clear()


        chart_data.extend(data)







# =====================================================
# SERVER START
# =====================================================

def run_server():


    global server_started


    global _server_thread



    if server_started:

        return



    server_started=True




    def _run():


        app.run(

            host=WEB_HOST,

            port=WEB_PORT,

            debug=False,

            use_reloader=False,

            threaded=True

        )




    _server_thread = threading.Thread(

        target=_run,

        daemon=True

    )



    _server_thread.start()



    print(

        f"[WEB SERVER START] http://{WEB_HOST}:{WEB_PORT}"

    )



    add_log(

        "WEB SERVER STARTED"

    )







# =====================================================
# RESET
# =====================================================

def reset_status():


    with status_lock:


        symbol=status["symbol"]


        status.clear()



        status.update({

            "mode":
                "DEMO",

            "symbol":
                symbol,

            "bot":
                "STOPPED",

            "position":
                "NONE",

            "position_size":
                0,

            "entry_price":
                0,

            "pnl":
                0

        })



    add_log(

        "STATUS RESET"

    )







def clear_logs():


    with log_lock:


        logs.clear()







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

    "get_trading_symbol",

    "update_chart",

    "reset_status",

    "clear_logs"

]







if __name__=="__main__":


    run_server()


    while True:

        time.sleep(1)
