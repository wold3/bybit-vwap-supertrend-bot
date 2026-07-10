from api.bybit_api import bybit_api


print("==============================")
print("DEMO ORDER TEST")
print("==============================")


# 현재 레버리지 확인
bybit_api.set_leverage()



# BUY 테스트
result = bybit_api.create_order(

    "Buy",

    "0.001"

)



print("==============================")

print("RESULT")

print(result)

print("==============================")
