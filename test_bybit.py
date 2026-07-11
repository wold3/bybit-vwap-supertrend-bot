# =====================================================
# BYBIT API TEST
# =====================================================

from api.bybit_api import bybit_api



print("====================")
print("BYBIT TEST START")
print("====================")



print()

print("STATUS")

print(
    bybit_api.status()
)



print()

print("PRICE")

print(
    bybit_api.get_price()
)



print()

print("BALANCE")

print(
    bybit_api.get_balance()
)



print()

print("POSITION")

print(
    bybit_api.get_position()
)



print()

print("====================")
print("TEST END")
print("====================")
