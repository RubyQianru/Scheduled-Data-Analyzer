from datetime import datetime, timedelta
from statistics import mean
from pymongo import MongoClient
from config import MONGO_URI, CRYPTO_DB, USERNAME, PASSWORD, TWITTER_DB, REPORT_DB
from util.text import clean_text, vader_sentiment
from datetime import datetime


client = MongoClient(MONGO_URI, username=USERNAME, password=PASSWORD)
crypto_db = client[CRYPTO_DB]
crypto_collection = crypto_db["crypto"]

twitter_db = client[TWITTER_DB]
twitter_collection = twitter_db["twitter"]

report_db = client[REPORT_DB]
report_collection = report_db["sentiment_report"]


def get_price(symbol:str = "BTC", days:int = 1):

  query = {"symbol": symbol}

  if days is not None:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    query["time"] = {
      "$gte": start_date,
      "$lte": end_date
    }

  pipeline = [
    {"$match": query},
    {"$group": {
        "_id": "$symbol",
        "mean_price": {"$avg": "$price"},
        "dayHigh": {"$max": "$dayHigh"},
        "dayLow": {"$min": "$dayLow"},
    }}
  ]
  
  data = list(crypto_collection.aggregate(pipeline))

  if data:
      stats = data[0]
      stats["_id"] = str(stats["_id"])
      return stats
  else:
      return None


def get_tweets(symbol:str = "BTC", days:int = 1):
  query = {"symbol": symbol}
  if days is not None:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    query["time"] = {
        "$gte": start_date,
        "$lte": end_date
    }

  data = list(twitter_collection.find(query).sort('timestamp', 1)) 
  vd_negative_scores = []
  vd_neutral_scores = []
  
  for item in data:
    item["_id"] = str(item["_id"])
    if 'time' in item:
        item['time'] = str(item['time'])
    if 'timestamp' in item:
        item['timestamp'] = str(item['timestamp'])
    if 'text' in item:
      text = clean_text(item['text'])
      neg, neu = vader_sentiment(text)
      vd_negative_scores.append(neg)
      vd_neutral_scores.append(neu)
  
  result = {
      "_id": symbol,
      "mean_vd_negative": mean(vd_negative_scores) if vd_negative_scores else None,
      "mean_vd_neutral": mean(vd_neutral_scores) if vd_neutral_scores else None
  }
   
  return result


def merge_results(price, twitter):
    merged_data = {}
    current_time = datetime.now()

    for item in price:
      merged_data[item] = price[item]
    for item in twitter:
      merged_data[item] = twitter[item]
    
    merged_data['symbol'] = merged_data['_id']
    merged_data['time'] = current_time
    del merged_data['_id']

    return merged_data


def insert_results(data):
  try:
    report_collection.insert_one(data)
  except Exception as e:
    print(f"Error in coin market API: {str(e)}")

