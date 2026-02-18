from flask import Blueprint, request, jsonify
from services.user_service import (
    get_all_users,
    create_user,
    update_user,
    delete_user
)

users_bp = Blueprint("users", __name__)


@users_bp.route("/health")
def health():
    return jsonify({"status": "Backend running"})


@users_bp.route("/users", methods=["GET"])
def get_users():
    users = get_all_users()
    return jsonify(users)


@users_bp.route("/users", methods=["POST"])
def add_user():
    data = request.json

    try:
        user_id = create_user(data["name"], data["email"])
        return jsonify({
            "id": user_id,
            "name": data["name"],
            "email": data["email"]
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def edit_user(user_id):
    data = request.json
    update_user(user_id, data["name"], data["email"])
    return jsonify({"message": "User updated"})


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    delete_user(user_id)
    return jsonify({"message": "User deleted"})
