from flask import Flask, request, redirect, send_from_directory, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__, static_folder="public")

# MongoDB connection (local)
client = MongoClient("mongodb://localhost:27017/")
db = client["assignment"]
collection = db["users"]

# Serve index.html
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# Handle form submit api
@app.route('/submit', methods=['POST'])
def submit():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        data = {
            "name": name,
            "email": email
        }
        collection.insert_one(data)
        return redirect('/success.html')
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3><a href='/'>Go Back</a>"

# Serve success page
@app.route('/success.html')
def success():
    return send_from_directory('public', 'success.html')

@app.route('/get', methods=['GET'])
def get_users():
    users = []
    for user in collection.find():
        user['_id'] = str(user['_id'])  # convert ObjectId to string
        users.append(user)
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True, port=3000)

# add new api data
