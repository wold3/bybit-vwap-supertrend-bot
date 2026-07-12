# =====================================================
# web/server.py
# VWAP SUPERTREND BOT
# WEB DASHBOARD SERVER
# =====================================================


from flask import Flask, jsonify, request

import threading
import time



# =====================================================
# FLASK
# =====================================================

app = Flask(
    __name__,
    static_folder="static",
    template_folder="."
)



# =====================================================
# GLOBAL DATA
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
# BOT CONNECT
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


    now = time.strftime(

        "%H:%M:%S"

    )


    text = f"[{now}] {msg}"


    print(text)


    _logs.append(text)



    if len(_logs) > 200:


        _logs.pop(0)







def update_status(data):


    _status.update(data)







# =====================================================
# TRADING MODE
# =====================================================

def get_trading_mode():


    try:


        from config import MODE


        return MODE



    except:


        return "DEMO"








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



        if data:


            return jsonify(data)



        return jsonify({


            "result":{

                "list":[]

            }


        })




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
# ORDER
# =====================================================

@app.route(
    "/api/order",
    methods=["POST"]
)

def api_order():


    try:


        data=request.json or {}



        side=data.get(

            "side"

        )


        qty=data.get(

            "qty"

        )



        if not _bot:


            return jsonify({

                "error":"BOT OFF"

            })





        if side=="Buy":


            result=_bot.order_manager.buy(

                qty

            )



        elif side=="Sell":


            result=_bot.order_manager.sell(

                qty

            )


        else:


            return jsonify({

                "error":"INVALID SIDE"

            })



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


        result=_bot.order_manager.close()



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


        _settings["leverage"]=data.get(

            "leverage",

            5

        )



        result=_bot.order_manager.set_leverage()



        return jsonify({

            "result":result

        })



    except Exception as e:


        return jsonify({

            "error":str(e)

        })








# =====================================================
# STOP LOSS
# =====================================================

@app.route(
    "/api/stoploss",
    methods=["POST"]
)

def api_stoploss():


    data=request.json or {}


    price=data.get(

        "price"

    )


    result=_bot.order_manager.set_stop_loss(

        price

    )


    return jsonify({

        "result":result

    })








# =====================================================
# TAKE PROFIT
# =====================================================

@app.route(
    "/api/takeprofit",
    methods=["POST"]
)

def api_takeprofit():


    data=request.json or {}



    price=data.get(

        "price"

    )


    result=_bot.order_manager.set_take_profit(

        price

    )



    return jsonify({

        "result":result

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



    _settings.update(

        data

    )


    add_log(

        "SETTINGS UPDATE"

    )



    return jsonify({

        "settings":_settings

    })









# =====================================================
# INDEX
# =====================================================

@app.route("/")

def index():


    return app.send_static_file(

        "index.html"

    )









# =====================================================
# SERVER RUN
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
