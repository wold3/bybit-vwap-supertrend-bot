# =====================================
# STRATEGY LOOP
# =====================================

def strategy_loop():


    print(
        "START STRATEGY LOOP"
    )


    while running:


        try:


            # 최신 시장 데이터

            market_data = (

                ws_client
                .get_latest_data()

            )



            if not market_data:


                time.sleep(1)

                continue





            signal = strategy_engine.check(

                market_data

            )



            if not signal:


                time.sleep(1)

                continue





            print(

                "STRATEGY SIGNAL",

                signal

            )





            # =================================
            # ENTRY
            # =================================

            if signal.get(
                "type"
            ) == "ENTRY":



                result = execution_engine.execute(

                    symbol=

                    signal["symbol"],


                    side=

                    signal["side"],


                    qty=

                    signal["qty"]

                )



                print(

                    "ENTRY RESULT",

                    result

                )







            # =================================
            # EXIT
            # =================================

            elif signal.get(
                "type"
            ) == "EXIT":



                position = (

                    position_manager
                    .get_position(

                        signal["symbol"]

                    )

                )



                if position:


                    execution_engine.close_position(

                        symbol=

                        signal["symbol"],


                        side=

                        position["side"],


                        qty=

                        position["size"]

                    )



        except Exception as e:


            print(

                "STRATEGY LOOP ERROR",

                e

            )



        time.sleep(1)
