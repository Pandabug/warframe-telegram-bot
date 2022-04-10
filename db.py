import os
from pymongo import MongoClient

client = MongoClient(os.environ.get(MONGODB_URL))
db = client['t_bot']
users_collection = db['users']