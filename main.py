import time
import threading


from config import (
    LIVE_TRADING,
    DEFAULT_SYMBOL,
    BYBIT_BASE_URL
)


from market.websocket_client import ws_client


from services.private_ws_client import private_ws_client


from portfolio.bybit_wallet import wallet


from execution.order_manager import order_manager


from strategy.strategy_engine import strategy_engine


from risk.risk_manager import risk_manager


from watchdog.watchdog import watchdog







def strategy_loop():


    print(
        "[START] STRATEGY LOOP"
    )


    while True:


        try:


            # 일일 손실 체크

            if not risk_manager.check_daily_loss():

                print(
                    "[STRATEGY STOP] RISK LIMIT"
                )

                break



            time.sleep(1)



        except Exception as e:


            print(
                "[STRATEGY LOOP ERROR]",
                e
            )


            time.sleep(3)









def start_bot():


    print("====================================")
    print("VWAP SUPERTREND BOT START")
    print("LIVE :", LIVE_TRADING)
    print("SYMBOL :", DEFAULT_SYMBOL)
    print("BASE :", BYBIT_BASE_URL)
    print("====================================")





    # -----------------------------
    # WATCHDOG
    # -----------------------------

    watchdog.start()





    # -----------------------------
    # WALLET INIT
    # -----------------------------


    equity = wallet.get_equity()



    print(
        "[ACCOUNT EQUITY]",
        equity
    )



    # ★ 추가된 부분
    # Risk Manager 초기 자산 저장

    risk_manager.initialize()







    # -----------------------------
    # WEBSOCKET START
    # -----------------------------


    public_thread = threading.Thread(

        target=ws_client.start,

        daemon=True

    )


    public_thread.start()





    private_thread = threading.Thread(

        target=private_ws_client.start,

        daemon=True

    )


    private_thread.start()







    # -----------------------------
    # STRATEGY
    # -----------------------------


    strategy_thread = threading.Thread(

        target=strategy_loop,

        daemon=True

    )


    strategy_thread.start()





    print(
        "[BOT RUNNING]"
    )









def stop_bot():


    print(
        "\n[BOT STOPPING]"
    )



    try:

        ws_client.stop()

    except:

        pass



    try:

        private_ws_client.stop()

    except:

        pass



    try:

        watchdog.stop()

    except:

        pass



    print(
        "[BOT STOPPED]"
    )








if __name__ == "__main__":


    try:


        start_bot()



        while True:


            time.sleep(1)



    except KeyboardInterrupt:


        stop_bot()
