from pymongo import MongoClient

client = MongoClient(MONGODB_URL)
db = client['t_bot']
users_collection = db['users']