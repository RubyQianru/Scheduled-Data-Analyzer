from util.util import get_price, get_tweets, merge_results, insert_results
from util.coins import coins

if __name__ == "__main__":
    for item in coins:
      price_data = get_price(symbol=item['symbol'])
      tweet_data = get_tweets(symbol=item['symbol'])
      merged_data = merge_results(price_data, tweet_data)
      insert_results(merged_data)