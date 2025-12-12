# app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# Read Mongo connection settings from env vars
MONGO_USER = os.environ.get("MONGO_INITDB_ROOT_USERNAME") or os.environ.get("MONGO_USER")
MONGO_PASS = os.environ.get("MONGO_INITDB_ROOT_PASSWORD") or os.environ.get("MONGO_PASS")
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
MONGO_DB = os.environ.get("MONGO_DB", "flask_db")

# Build connection URI
if MONGO_USER and MONGO_PASS:
    mongo_uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
else:
    mongo_uri = os.environ.get("MONGODB_URI", f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")

client = MongoClient(mongo_uri)
db = client[MONGO_DB]
collection = db.data

@app.route('/')
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        payload = request.get_json(force=True)
        collection.insert_one(payload)
        return jsonify({"status": "Data inserted"}), 201
    else:
        docs = list(collection.find({}, {"_id": 0}))
        return jsonify(docs), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
