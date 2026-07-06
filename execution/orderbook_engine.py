class OrderBookEngine:

    def __init__(self):
        self.books = {}

    def update(self, symbol, bids, asks):

        self.books[symbol] = {
            "bids": bids,
            "asks": asks
        }

    def mid_price(self, symbol):

        book = self.books.get(symbol)

        if not book:
            return None

        try:
            bid = float(book["bids"][0][0])
            ask = float(book["asks"][0][0])
            return (bid + ask) / 2

        except:
            return None

    def liquidity_score(self, symbol):

        book = self.books.get(symbol)

        if not book:
            return 0

        try:
            bid = sum(float(x[1]) for x in book["bids"][:5])
            ask = sum(float(x[1]) for x in book["asks"][:5])
            return bid + ask

        except:
            return 0


orderbook_engine = OrderBookEngine()
