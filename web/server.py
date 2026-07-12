# =====================================================
# web/server.py
# VWAP SUPERTREND BOT
# WEB SERVER + GLOBAL STATE
# =====================================================


from flask import Flask, jsonify, request, send_from_directory

import os
import time
import threading



# =====================================================
# APP
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


app = Flask(
    __name__,
    static_folder=os.path.join(
        BASE_DIR,
        "web",
        "static"
    )
)



# =====================================================
# GLOBAL
# =====================================================

_bot = None


_logs = []


_status = {


    "api":"OK",
    "bot":"STOPPED",
    "mode":"DEMO",
    "symbol":"BTCUSDT",
    "position":"NONE",
    "position_size":0,
    "entry_price":0,
    "price":0,
    "mark_price":0,
    "pnl":0,
    "liq_price":0,
    "last_action":""

}



_settings = {


    "leverage":5,
    "stop_loss":2,
    "take_profit":3,

    "buy1":50,
    "buy2":50,

    "tp1":30,
    "tp2":30,
    "tp3":40

}





# =====================================================
# BOT LINK
# =====================================================

def set_bot(bot):

    global _bot

    _bot = bot

    add_log(
        f"BOT {bot}"
    )



def get_bot():

    return _bot






# =====================================================
# LOG
# =====================================================

def add_log(msg):

    text = (

        "["

        +

        time.strftime("%H:%M:%S")

        +

        "] "

        +

        str(msg)

    )


    print(text)


    _logs.append(text)



    if len(_logs)>300:

        _logs.pop(0)






# =====================================================
# STATUS
# =====================================================

def update_status(data):

    if data:

        _status.update(data)



def get_status():

    return _status




def get_logs():

    return _logs






# =====================================================
# MODE
# =====================================================

def get_trading_mode():

    try:

        from config import MODE

        return MODE


    except:

        return "DEMO"






# =====================================================
# SYMBOL
# =====================================================

def get_trading_symbol():

    try:

        from config import SYMBOL

        return SYMBOL


    except:

        return "BTCUSDT"








# =====================================================
# SETTINGS
# =====================================================

def get_settings():

    return _settings







# =====================================================
# STATUS API
# =====================================================

@app.route("/api/status")

def api_status():

    return jsonify({

        "logs":_logs[-100:],

        "status":_status,

        "settings":_settings

    })







# =====================================================
# CANDLE API
# =====================================================

@app.route("/api/candles")

def api_candles():

    try:


        from api.bybit_api import bybit_api


        data = bybit_api.get_kline(

            interval="5",

            limit=100

        )


        return jsonify(data)



    except Exception as e:


        add_log(
            f"CANDLE ERROR {e}"
        )


        return jsonify({

            "result":{

                "list":[]

            }

        })









# =====================================================
# ORDER API
# =====================================================

@app.route(
    "/api/order",
    methods=["POST"]
)

def api_order():

    try:

        data=request.json or {}


        side=data.get("side")

        qty=data.get(
            "qty",
            None
        )


        if not _bot:

            return jsonify({

                "error":"BOT OFF"

            })



        result = _bot.order_manager.open_position(

            side,

            qty

        )


        return jsonify({

            "result":result

        })


    except Exception as e:


        add_log(
            f"ORDER ERROR {e}"
        )


        return jsonify({

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

        result=_bot.order_manager.close_position()


        return jsonify({

            "result":result

        })


    except Exception as e:


        return jsonify({

            "error":str(e)

        })









# =====================================================
# LEVERAGE
# =====================================================

@app.route(
    "/api/leverage",
    methods=["POST"]
)

def api_leverage():

    try:

        data=request.json or {}


        _settings["leverage"] = data.get(

            "leverage",

            5

        )


        return jsonify({

            "result":True

        })


    except Exception as e:


        return jsonify({

            "error":str(e)

        })









# =====================================================
# SETTINGS
# =====================================================

@app.route(
    "/api/settings",
    methods=["POST"]
)

def api_settings():

    data=request.json or {}


    _settings.update(data)


    add_log(
        "SETTINGS UPDATED"
    )


    return jsonify({

        "settings":_settings

    })








# =====================================================
# INDEX
# =====================================================

@app.route("/")

def index():

    return send_from_directory(

        os.path.join(

            BASE_DIR,

            "web"

        ),

        "index.html"

    )








# =====================================================
# SERVER START
# =====================================================

def run_server():


    add_log(
        "WEB SERVER START"
    )


    app.run(

        host="0.0.0.0",

        port=8000,

        debug=False,

        use_reloader=False

    )
