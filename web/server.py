# =====================================================
# web/server.py
# VWAP SUPERTREND BOT
# WEB SERVER
# =====================================================

from flask import (
    Flask,
    jsonify,
    request,
    send_file,
    send_from_directory
)

import os
import time
import threading


app = Flask(__name__)



# =====================================================
# GLOBAL
# =====================================================

BASE_DIR = os.path.dirname(__file__)


logs = []


status = {

    "api": "OK",

    "bot": "STOPPED",

    "mode": "DEMO",

    "symbol": "BTCUSDT",

    "price": 0,

    "position": "NONE",

    "position_size": 0,

    "entry_price": 0,

    "mark_price": 0,

    "liq_price": 0,

    "pnl": 0,

    "last_action": "",

    "watchdog": "OFF"

}



bot_instance = None


trading_mode = "DEMO"

trading_symbol = "BTCUSDT"







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


    if isinstance(data,dict):

        status.update(data)






def get_status():

    return status.copy()







# =====================================================
# BOT
# =====================================================

def set_bot(bot):

    global bot_instance


    bot_instance = bot


    status["bot"] = "RUNNING"


    add_log(

        f"BOT {bot}"

    )



    return True





def get_bot():

    return bot_instance







# =====================================================
# MODE
# =====================================================

def get_trading_mode():

    return trading_mode






def set_trading_mode(mode):

    global trading_mode


    trading_mode = str(mode).upper()


    status["mode"] = trading_mode


    return True







# =====================================================
# SYMBOL
# =====================================================

def get_trading_symbol():

    return trading_symbol






def set_trading_symbol(symbol):

    global trading_symbol


    trading_symbol = str(symbol).upper()


    status["symbol"] = trading_symbol


    return True







# =====================================================
# HOME
# =====================================================

@app.route("/")

def index():


    return send_file(

        os.path.join(

            BASE_DIR,

            "index.html"

        )

    )







# =====================================================
# CHART.JS
# =====================================================

@app.route("/chart.js")

def chart_file():


    return send_from_directory(

        BASE_DIR,

        "chart.js"

    )







# =====================================================
# STATUS API
# =====================================================

@app.route("/api/status")

def api_status():


    return jsonify({

        "status":status,

        "logs":logs[-100:]

    })








@app.route("/api/logs")

def api_logs():


    return jsonify(logs)









# =====================================================
# CANDLE API
# =====================================================

@app.route("/api/candles")

def api_candles():


    try:


        from api.bybit_api import bybit_api



        result = bybit_api.get_kline(

            interval="5",

            limit=100

        )


        return jsonify(result)



    except Exception as e:


        add_log(

            f"CANDLE ERROR {e}"

        )


        return jsonify({})









# =====================================================
# ORDER
# =====================================================

@app.route(

    "/api/order",

    methods=["POST"]

)

def api_order():


    try:


        data=request.json



        side=data.get(

            "side"

        )


        qty=data.get(

            "qty",

            0.001

        )



        from order.order_manager import order_manager



        result = order_manager.open_position(

            side,

            qty

        )



        return jsonify({

            "success":

            bool(result)

        })




    except Exception as e:


        add_log(

            f"ORDER ERROR {e}"

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
# FAVICON
# =====================================================

@app.route("/favicon.ico")

def favicon():


    return "",204







# =====================================================
# SERVER START
# =====================================================

def run_server():


    app.run(

        host="0.0.0.0",

        port=8000,

        debug=False,

        use_reloader=False

    )







def start_server():


    t = threading.Thread(

        target=run_server,

        daemon=True

    )


    t.start()


    add_log(

        "WEB SERVER START"

    )
