# =====================================================
# STATUS API
# =====================================================

@app.route("/api/status")
def api_status():


    return jsonify({


        "logs": _logs[-100:],


        "status": _status


    })







# =====================================================
# CANDLE API
# =====================================================

@app.route("/api/candles")
def api_candles():


    try:


        if _bot:


            data = _bot.market_data.get_candles()


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
# ORDER API
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

            "qty"

        )





        if not _bot:


            return jsonify({

                "error":

                "BOT OFF"

            })





        if side=="Buy":


            result = _bot.order_manager.buy(

                qty

            )



        elif side=="Sell":


            result = _bot.order_manager.sell(

                qty

            )


        else:


            return jsonify({

                "error":

                "INVALID SIDE"

            })





        return jsonify({

            "result":

            result

        })




    except Exception as e:


        add_log(

            f"ORDER API ERROR {e}"

        )


        return jsonify({

            "error":

            str(e)

        })









# =====================================================
# CLOSE API
# =====================================================

@app.route(

    "/api/close",

    methods=["POST"]

)

def api_close():


    try:


        result = _bot.order_manager.close()



        return jsonify({

            "result":

            result

        })



    except Exception as e:


        return jsonify({

            "error":

            str(e)

        })









# =====================================================
# LEVERAGE API
# =====================================================

@app.route(

    "/api/leverage",

    methods=["POST"]

)

def api_leverage():


    try:


        data=request.json



        _settings["leverage"] = data.get(

            "leverage",

            5

        )



        result = _bot.order_manager.set_leverage()



        return jsonify({

            "result":

            result

        })



    except Exception as e:


        return jsonify({

            "error":

            str(e)

        })

# =====================================================
# STOP LOSS API
# =====================================================

@app.route(
    "/api/stoploss",
    methods=["POST"]
)
def api_stoploss():


    try:


        data = request.json



        price = data.get(
            "price"
        )



        percent = data.get(
            "percent"
        )



        _settings["stop_loss"] = percent



        result = _bot.order_manager.set_stop_loss(

            price

        )



        return jsonify({

            "result":

            result

        })



    except Exception as e:


        add_log(

            f"STOPLOSS ERROR {e}"

        )


        return jsonify({

            "error":

            str(e)

        })









# =====================================================
# TAKE PROFIT API
# =====================================================

@app.route(
    "/api/takeprofit",
    methods=["POST"]
)
def api_takeprofit():


    try:


        data=request.json



        price=data.get(

            "price"

        )



        result = _bot.order_manager.set_take_profit(

            price

        )



        return jsonify({

            "result":

            result

        })



    except Exception as e:


        return jsonify({

            "error":

            str(e)

        })









# =====================================================
# SETTINGS API
# =====================================================

@app.route(
    "/api/settings",
    methods=["POST"]
)
def api_settings():


    try:


        data=request.json



        _settings.update(

            data

        )



        add_log(

            "SETTINGS UPDATED"

        )



        return jsonify({

            "settings":

            _settings

        })



    except Exception as e:


        return jsonify({

            "error":

            str(e)

        })









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
# RUN SERVER
# =====================================================

def run_server():


    app.run(

        host="0.0.0.0",

        port=8000,

        debug=False,

        use_reloader=False

    )
