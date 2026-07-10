# =====================================================
# web/chart_data.py
# Chart Data Store
# =====================================================


candles = []



def add_candle(data):


    candles.append(data)



    if len(candles) > 200:

        candles.pop(0)




def get_candles():


    return candles
