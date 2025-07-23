# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from pymongo import MongoClient
# from bson.objectid import ObjectId

# app = Flask(__name__)
# CORS(app)

# # Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# db = client["userdb"]
# collection = db["users"]

# # ✅ Helper to serialize MongoDB document safely
# def serialize_user(user):
#     return {
#         "id": str(user["_id"]),  # Match frontend's 'id' field
#         "name": user.get("name", ""),
#         "age": user.get("age", None)
#     }

# # ✅ Get all users
# @app.route("/users", methods=["GET"])
# def get_users():
#     users = [serialize_user(user) for user in collection.find()]
#     return jsonify({"users": users}), 200

# # ✅ Add a new user
# @app.route("/users", methods=["POST"])
# def add_user():
#     data = request.get_json()
#     name = data.get("name")
#     age = data.get("age")

#     if not name or age is None:
#         return jsonify({"error": "Name and age are required"}), 400

#     result = collection.insert_one({"name": name, "age": age})
#     return jsonify({"message": "User added", "id": str(result.inserted_id)}), 201

# # ✅ Update a user
# @app.route("/users/<string:user_id>", methods=["PUT"])
# def update_user(user_id):
#     data = request.get_json()
#     name = data.get("name")
#     age = data.get("age")

#     if not name or age is None:
#         return jsonify({"error": "Name and age are required"}), 400

#     try:
#         result = collection.update_one(
#             {"_id": ObjectId(user_id)},
#             {"$set": {"name": name, "age": age}}
#         )
#         if result.matched_count == 0:
#             return jsonify({"error": "User not found"}), 404
#         return jsonify({"message": "User updated"}), 200
#     except:
#         return jsonify({"error": "Invalid ID format"}), 400

# # ✅ Delete a user
# @app.route("/users/<string:user_id>", methods=["DELETE"])
# def delete_user(user_id):
#     try:
#         result = collection.delete_one({"_id": ObjectId(user_id)})
#         if result.deleted_count == 1:
#             return jsonify({"message": "User deleted"}), 200
#         return jsonify({"error": "User not found"}), 404
#     except:
#         return jsonify({"error": "Invalid ID format"}), 400

# # ✅ Start the server
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (needed for Streamlit frontend)

# Simulated "Database"
data_store = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

# Auto-increment ID
next_id = 3


@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify(data_store), 200


@app.route('/add_data', methods=['POST'])
def add_data():
    global next_id
    item = request.get_json()
    item["id"] = next_id
    data_store.append(item)
    next_id += 1
    return jsonify({"message": "Data added successfully"}), 201


@app.route('/update_data/<int:item_id>', methods=['PUT'])
def update_data(item_id):
    updated_item = request.get_json()
    for item in data_store:
        if item["id"] == item_id:
            item["name"] = updated_item.get("name", item["name"])
            item["email"] = updated_item.get("email", item["email"])
            return jsonify({"message": "Data updated"}), 200
    return jsonify({"message": "Item not found"}), 404


@app.route('/delete_data/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    global data_store
    data_store = [item for item in data_store if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200


if __name__ == 'main':
    app.run(host='0.0.0.0', port=5000)