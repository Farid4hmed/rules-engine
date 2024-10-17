from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['rule_engine_db']
rules_collection = db['rules']

def insert_rule(rule_data):
    result = rules_collection.insert_one(rule_data)
    return result.inserted_id

def get_rule(rule_id):
    return rules_collection.find_one({'_id': ObjectId(rule_id)})

def get_rules(rule_ids):
    object_ids = [ObjectId(rid) for rid in rule_ids]
    return list(rules_collection.find({'_id': {'$in': object_ids}}))