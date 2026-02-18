from flask import Blueprint, request, jsonify
from db import get_db_connection
import mysql.connector

users_bp = Blueprint("users", __name__)

@users_bp.route("/health")
def health():
    return jsonify({"status": "Backend running"})

@users_bp.route("/users", methods=["GET"])
def get_users():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        print("Connecting to mysql")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("select * from users")
        users = cursor.fetchall()
        return jsonify(users)
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("insert into users (name,email) values (%s, %s)",
                    (data["name"], data["email"]))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            "id": user_id,
            "name": data["name"],
            "email": data["email"]
        }), 201
    except mysql.connector.Error as err:
        if err.errno == 1062:
            return jsonify({"error": "Email already exists"}), 400
        return jsonify({"error": str(err)}), 400
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data= request.json
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name=%s, email=%s where id=%s",
            (data["name"], data["email"], user_id)
        )
        conn.commit()
        return jsonify({"message": "User updated"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@users_bp.route("/users/<int:user_id>", methods = ["DELETE"])
def delete_user(user_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE from users where id=%s", (user_id,)
        )
        conn.commit()
        return jsonify({"message": "User deleted"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()