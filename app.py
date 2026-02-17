from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

users =[]
current_id = 1

@app.route("/health")
def health():
    return jsonify({"status": "Backend running"})

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/users", methods=["POST"])
def create_user():
    global current_id
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email required"}), 400
    user = {
        "id": current_id,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(user)
    current_id += 1

    return jsonify(user), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data= request.json
    for user in users:
        if user["id"] == user_id:
            user["name"] = data.get("name", user["name"])
            user["email"] = data.get("email", user["email"])
            return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route("/users/<int:user_id>", methods = ["DELETE"])
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)