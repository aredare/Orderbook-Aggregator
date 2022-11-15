import requests
import json
# The following is a Python class implementation for an order book aggregator that fetches BTC order books from Gemini,
# Kraken and CoinBase Pro cryptocurrency exchanges and prints out the price to buy 10 bitcoin and sell 10 bitcoin.
# Price for taking liquidity will be determined as the price level on each side where the order can be fully executed.


class AggregatedOrderbookBTC:  # Order book Aggregator Class for BTC
    def __init__(self):
        self.bids = []
        self.asks = []
        self.taker_bid = 0
        self.taker_ask = 0

        self.start()   # Initialize the order book aggregator

    def start(self):
        coinbase_bids, coinbase_asks = self.get_coinbase_orderbook()
        gemini_bids, gemini_asks = self.get_gemini_orderbook()
        kraken_bids, kraken_asks = self.get_kraken_orderbook()

        self.update(coinbase_bids, coinbase_asks)
        self.update(gemini_bids, gemini_asks)
        self.update(kraken_bids, kraken_asks)

    def update(self, _bids, _asks):
        self.bids += _bids     # Merge new bids with existing bids
        self.asks += _asks     # Merge new asks with existing asks

        self.bids.sort(key=lambda x: float(x[0]), reverse=True)  # Sorting the bids in descending order
        self.asks.sort(key=lambda x: float(x[0]))                # Sorting the asks in ascending order

    def compute_taker_market(self, quantity):
        amount_sum = 0

        for bid in self.bids:
            if amount_sum > quantity:    # if the cumulative BTC amount sum exceeds the request quantity
                self.taker_bid = bid[0]  # The limit price that ensures the total quantity of a sale will be executed
                break
            amount_sum += float(bid[1])

        amount_sum = 0

        for ask in self.asks:
            if amount_sum > quantity:     # if the cumulative BTC amount sum exceeds the request quantity
                self.taker_ask = ask[0]   # The taker price that ensures the total quantity of a buy will be executed
                break
            amount_sum += float(ask[1])

    def get_taker_market(self, quantity):    # Return market quotes for taking liquidity
        self.compute_taker_market(quantity)

        return self.taker_bid, self.taker_ask

    @staticmethod
    def get_coinbase_orderbook():  # Retrieves the Level 2 order from Coinbase (Full aggregated order book).
        url = "https://api.exchange.coinbase.com/products/{0}/book?level=2".format("BTC-USD")
        response = requests.get(url)

        return response.json()["bids"], response.json()["asks"]

    @staticmethod
    def get_gemini_orderbook():   # Retrieves the full aggregated order book from Gemini.
        url = "https://api.gemini.com/v1/book/{0}".format("btcusd")
        response = requests.get(url)

        gemini_bids = []
        for priceLevel in response.json()['bids']:
            gemini_bids.append([priceLevel['price'], priceLevel['amount']])

        gemini_asks = []
        for priceLevel in response.json()['asks']:
            gemini_asks.append([priceLevel['price'], priceLevel['amount']])

        return gemini_bids, gemini_asks  # returns bids and asks in the form of list of lists.

    @staticmethod
    def get_kraken_orderbook():  # Retrieves the full aggregated order book from Kraken
        url = "https://api.kraken.com/0/public/Depth?pair={0}".format("XBTUSD")
        response = requests.get(url)
        kraken_product_id = list(response.json()['result'].keys())[0]  # product id differs from id used in GET request
        # returns bids and asks in the form of list of lists.
        return response.json()['result'][kraken_product_id]["bids"], response.json()['result'][kraken_product_id]["asks"]

    def check_sorted(self):       # Sanity check to ensure that the merged bids and asks are sorted correctly.
        for i in range(1, len(self.bids)):
            if float(self.bids[i][0]) > float(self.bids[i-1][0]):
                return False

        for i in range(1, len(self.asks)):
            if float(self.asks[i][0]) < float(self.asks[i-1][0]):
                return False

        return True


requested_quantity = input("Welcome!\n\nHow much BitCoin do you want to buy or sell? ")   # User input for BTC size

if float(requested_quantity) < 0.01:
    print("\nRequested quantity lower than minimum order size allowed.")

elif 0.01 <= float(requested_quantity) <= 250:
    btc_aggregated_book = AggregatedOrderbookBTC()

    if btc_aggregated_book.check_sorted():
        taker_bid, taker_ask = btc_aggregated_book.get_taker_market(float(requested_quantity))

        print("\n=================================================================================\n"
              " Taker Prices to buy and sell {0} BTC to guarantee execution\n To Sell ".format(requested_quantity),
              requested_quantity, " => $", taker_bid, "\n To Buy  ", requested_quantity, " => $", taker_ask,
              "\n=================================================================================")

else:
    print("\nRequested quantity higher that maximum order size allowed.")
