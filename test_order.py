from api.bybit_api import bybit_api


print("==============================")
print("DEMO ORDER TEST")
print("==============================")


price = bybit_api.get_price()

print(
    "CURRENT PRICE :",
    price
)


tp = price * 1.01

sl = price * 0.995



result = bybit_api.create_order(

    side="Buy",

    qty=0.001,

    take_profit=tp,

    stop_loss=sl

)



print("==============================")
print(result)
print("==============================")
