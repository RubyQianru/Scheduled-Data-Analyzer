from util.util import get_price, get_tweets, merge_results, insert_results, get_sma
from util.coins import coins

if __name__ == "__main__":
    for item in coins:
      sma_data = get_sma(symbol=item['symbol'])
