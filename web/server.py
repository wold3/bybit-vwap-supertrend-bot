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
