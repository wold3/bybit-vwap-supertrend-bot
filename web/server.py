# =====================================================
# web/server.py
# WEB DASHBOARD SERVER
# =====================================================

from flask import (
    Flask,
    render_template,
    jsonify,
    request
)

import threading
import time

app = Flask(
    __name__,
    template_folder="templates"
)

# =====================================================
# GLOBAL
# =====================================================

bot_instance = None

server_started = False

trading_mode = "DEMO"

MAX_LOGS = 500

status = {

    "mode": "DEMO",

    "bot": "STOPPED",

    "position": "NONE",

    "position_size": 0,

    "entry_price": 0,

    "pnl": 0,

    "price": 0,

    "balance": 0,

    "equity": 0

}

logs = []

status_lock = threading.Lock()

log_lock = threading.Lock()


# =====================================================
# LOG
# =====================================================

def add_log(message):

    now = time.strftime("%H:%M:%S")

    text = f"[{now}] {message}"

    print(text)

    with log_lock:

        logs.append(text)

        while len(logs) > MAX_LOGS:

            logs.pop(0)


# =====================================================
# STATUS
# =====================================================

def update_status(data):

    with status_lock:

        status.update(data)


def get_status():

    with status_lock:

        return status.copy()


# =====================================================
# BOT
# =====================================================

def set_bot_instance(bot):

    global bot_instance

    bot_instance = bot


# =====================================================
# MODE
# =====================================================

def get_trading_mode():

    return trading_mode


# =====================================================
# HOME
# =====================================================

@app.route("/")

def index():

    return render_template("dashboard.html")


# =====================================================
# STATUS API
# =====================================================

@app.route("/api/status")

def api_status():

    return jsonify({

        "status": get_status(),

        "logs": logs[-100:]

    })


# =====================================================
# LOG API
# =====================================================

@app.route("/api/logs")

def api_logs():

    return jsonify({

        "logs": logs

    })

# =====================================================
# START
# =====================================================

@app.route(

    "/api/start",

    methods=["POST"]

)

def api_start():

    global bot_instance

    try:

        if bot_instance is None:

            return jsonify({

                "success": False,

                "error": "BOT NOT READY"

            })

        if get_status()["bot"] == "RUNNING":

            return jsonify({

                "success": True,

                "message": "ALREADY RUNNING"

            })

        bot_instance.start()

        update_status({

            "bot": "RUNNING"

        })

        add_log("BOT START")

        return jsonify({

            "success": True

        })

    except Exception as e:

        add_log(

            f"START ERROR {e}"

        )

        return jsonify({

            "success": False

        })


# =====================================================
# STOP
# =====================================================

@app.route(

    "/api/stop",

    methods=["POST"]

)

def api_stop():

    global bot_instance

    try:

        if bot_instance:

            bot_instance.stop()

        update_status({

            "bot": "STOPPED"

        })

        add_log(

            "BOT STOP"

        )

        return jsonify({

            "success": True

        })

    except Exception as e:

        add_log(

            f"STOP ERROR {e}"

        )

        return jsonify({

            "success": False

        })


# =====================================================
# RESTART
# =====================================================

@app.route(

    "/api/restart",

    methods=["POST"]

)

def api_restart():

    global bot_instance

    try:

        if bot_instance:

            bot_instance.stop()

            time.sleep(1)

            bot_instance.start()

        update_status({

            "bot": "RUNNING"

        })

        add_log(

            "BOT RESTART"

        )

        return jsonify({

            "success": True

        })

    except Exception as e:

        add_log(

            f"RESTART ERROR {e}"

        )

        return jsonify({

            "success": False

        })


# =====================================================
# MODE CHANGE
# =====================================================

@app.route(

    "/api/mode",

    methods=["POST"]

)

def api_mode():

    global trading_mode

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

            "success": False,

            "error": "INVALID MODE"

        })

    trading_mode = mode

    update_status({

        "mode": mode

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

            f"MODE API ERROR {e}"

        )

    return jsonify({

        "success": True,

        "mode": mode

    })


# =====================================================
# CLOSE POSITION
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

            "success": bool(result)

        })

    except Exception as e:

        add_log(

            f"CLOSE ERROR {e}"

        )

        return jsonify({

            "success": False

        })


# =====================================================
# RESET STATUS
# =====================================================

@app.route(

    "/api/reset",

    methods=["POST"]

)

def api_reset():

    update_status({

        "position": "NONE",

        "position_size": 0,

        "entry_price": 0,

        "pnl": 0

    })

    add_log(

        "STATUS RESET"

    )

    return jsonify({

        "success": True

    })

# =====================================================
# PING
# =====================================================

@app.route(

    "/api/ping"

)

def api_ping():

    return jsonify({

        "success": True,

        "server": "running",

        "time": int(time.time())

    })


# =====================================================
# SERVER THREAD
# =====================================================

_server_thread = None


def run_server():

    global server_started
    global _server_thread

    if server_started:

        return

    server_started = True

    def _run():

        app.run(

            host="0.0.0.0",

            port=8000,

            debug=False,

            use_reloader=False,

            threaded=True

        )

    _server_thread = threading.Thread(

        target=_run,

        daemon=True,

        name="WebServer"

    )

    _server_thread.start()

    print(

        "[WEB SERVER START] http://0.0.0.0:8000"

    )

    add_log(

        "WEB SERVER STARTED"

    )


# =====================================================
# STOP SERVER
# =====================================================

def stop_server():

    global server_started

    server_started = False

    add_log(

        "WEB SERVER STOP"

    )


# =====================================================
# CLEAR LOGS
# =====================================================

def clear_logs():

    with log_lock:

        logs.clear()

    add_log(

        "LOG CLEARED"

    )


# =====================================================
# RESET STATUS
# =====================================================

def reset_status():

    with status_lock:

        status.clear()

        status.update({

            "mode": trading_mode,

            "bot": "STOPPED",

            "position": "NONE",

            "position_size": 0,

            "entry_price": 0,

            "pnl": 0,

            "price": 0,

            "balance": 0,

            "equity": 0

        })

    add_log(

        "STATUS RESET"

    )


# =====================================================
# EXPORT
# =====================================================

__all__ = [

    "app",

    "run_server",

    "stop_server",

    "set_bot_instance",

    "update_status",

    "get_status",

    "add_log",

    "clear_logs",

    "reset_status",

    "get_trading_mode"

]


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    run_server()

    while True:

        time.sleep(1)
