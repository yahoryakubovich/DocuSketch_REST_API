from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# Подключение к MongoDB
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.mydb
collection = db.mydata


@app.route('/create', methods=['POST'])
def create_value():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    result = collection.insert_one({'key': key, 'value': value})
    return jsonify({'message': 'Value created successfully', 'id': str(result.inserted_id)})


@app.route('/update', methods=['PUT'])
def update_value():
    data = request.get_json()
    key = data.get('key')
    new_value = data.get('new_value')
    result = collection.update_one({'key': key}, {'$set': {'value': new_value}})
    if result.modified_count == 0:
        return jsonify({'message': 'Key not found'})
    return jsonify({'message': 'Value updated successfully'})


@app.route('/read/<key>', methods=['GET'])
def read_value(key):
    result = collection.find_one({'key': key})
    if result:
        return jsonify({'key': result['key'], 'value': result['value']})
    return jsonify({'message': 'Key not found'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
