import http.client
import json
from datetime import datetime
from pymongo import MongoClient
from config import MONGO_URI, CRYPTO_DB, USERNAME, PASSWORD, TWITTER_DB

client = MongoClient(MONGO_URI, username=USERNAME, password=PASSWORD)
crypto_db = client[CRYPTO_DB]
crypto_collection = crypto_db["crypto"]

twitter_db = client[TWITTER_DB]
twitter_collection = twitter_db["twitter"]

