from pymongo import MongoClient
import urllib.parse

def fetch_mongo_data(uri, db_name, collection_name):

    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    cursor = collection.find({})
    return cursor

def insert_sample_data(uri, db_name, collection_name, data):
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    result = collection.insert_many(data)
    print(f"Inserted {len(result.inserted_ids)} documents.")


sample_users = [
    {"country":"pk","host": "65.0.223.49", "user": "rbdbuser", "password": "Zaqxrw176!@#AHtR96", "db": "rbexplode_pk"},
    {"country":"sa","host": "65.0.223.49", "user": "rbdbuser", "password": "Zaqxrw176!@#AHtR96", "db": "rbexplode_sa"},
]

encoded_password = urllib.parse.quote_plus("+M77AQZZw$_4YAs")

Mongo_URI =f"mongodb+srv://rohankumar399:{encoded_password}@dailycheck.8kfzufy.mongodb.net/?retryWrites=true&w=majority&appName=DailyCheck"
Database ="DailyCheckDB"
Collection ="credentials"
docs=fetch_mongo_data(Mongo_URI,Database,Collection)

for i in docs:
    print(i)

# insert_sample_data(Mongo_URI, "DailyCheckDB", "credentials", sample_users)