# =====================================================
# web/server.py
# VWAP SUPERTREND BOT WEB SERVER
# BYBIT V5
# =====================================================

from flask import (
    Flask,
    jsonify,
    request,
    send_file
)

import threading
import time
import os



app = Flask(__name__)





# =====================================================
# GLOBAL STATE
# =====================================================

logs = []


status = {

    "bot": "STOPPED",

    "mode": "DEMO",

    "symbol": "BTCUSDT",

    "position": "NONE",

    "position_size": 0,

    "entry_price": 0,

    "pnl": 0,

    "last_action": ""

}



trading_mode = "DEMO"

trading_symbol = "BTCUSDT"

bot_status = "STOPPED"






# =====================================================
# LOG
# =====================================================

def add_log(message):


    text = (

        time.strftime("[%H:%M:%S] ")

        +

        str(message)

    )


    print(text)


    logs.append(text)



    if len(logs) > 300:

        logs.pop(0)






# =====================================================
# STATUS
# =====================================================

def update_status(data):


    if isinstance(data, dict):

        status.update(data)






def get_status():

    return status.copy()






# =====================================================
# BOT CONTROL
# =====================================================

def set_bot(value):


    global bot_status


    bot_status = value


    status["bot"] = value


    add_log(

        f"BOT STATUS {value}"

    )


    return True






def get_bot():

    return bot_status







# =====================================================
# TRADING MODE
# =====================================================

def get_trading_mode():


    return trading_mode






def set_trading_mode(mode):


    global trading_mode


    if mode in (

        "DEMO",

        "LIVE"

    ):


        trading_mode = mode


        status["mode"] = mode


        add_log(

            f"MODE {mode}"

        )


        return True



    return False







# =====================================================
# SYMBOL
# =====================================================

def get_trading_symbol():


    return trading_symbol






def set_trading_symbol(symbol):


    global trading_symbol


    trading_symbol = str(symbol).upper()


    status["symbol"] = trading_symbol


    add_log(

        f"SYMBOL {trading_symbol}"

    )


    return True







# =====================================================
# HOME
# =====================================================

@app.route("/")

def home():


    path = os.path.join(

        os.path.dirname(__file__),

        "index.html"

    )


    if os.path.exists(path):

        return send_file(path)


    return "VWAP SUPERTREND BOT"








# =====================================================
# STATUS API
# =====================================================

@app.route("/api/status")

def api_status():


    return jsonify({

        "status": status,

        "logs": logs[-100:]

    })







@app.route("/api/logs")

def api_logs():


    return jsonify(logs)







# =====================================================
# ORDER API
# =====================================================

@app.route(

    "/api/order",

    methods=["POST"]

)

def api_order():


    try:


        data = request.json


        side = data.get(

            "side"

        )


        qty = data.get(

            "qty"

        )



        from order.order_manager import order_manager



        result = order_manager.open_position(

            side,

            qty

        )



        return jsonify({

            "success":

                bool(result),

            "result":

                str(result)

        })



    except Exception as e:


        add_log(

            f"WEB ORDER ERROR {e}"

        )


        return jsonify({

            "success":False,

            "error":str(e)

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


        return jsonify({

            "success":

                bool(result)

        })



    except Exception as e:


        add_log(

            f"CLOSE ERROR {e}"

        )


        return jsonify({

            "success":False

        })








# =====================================================
# BOT START STOP
# =====================================================

@app.route(

    "/api/start",

    methods=["POST"]

)

def api_start():


    set_bot(

        "RUNNING"

    )


    return jsonify({

        "success":True

    })






@app.route(

    "/api/stop",

    methods=["POST"]

)

def api_stop():


    set_bot(

        "STOPPED"

    )


    return jsonify({

        "success":True

    })







# =====================================================
# SERVER START
# =====================================================

def start_server():


    thread = threading.Thread(

        target=lambda:

            app.run(

                host="0.0.0.0",

                port=8000,

                debug=False,

                use_reloader=False

            ),

        daemon=True

    )


    thread.start()


    add_log(

        "WEB SERVER START"

    )
