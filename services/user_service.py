from db.connection import connect_to_db
import mysql.connector


def get_all_users():
    db = connect_to_db()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    finally:
        cursor.close()
        db.close()


def create_user(name, email):
    db = connect_to_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (name, email)
        )
        db.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        if err.errno == 1062:
            raise ValueError("Email already exists")
        raise err
    finally:
        cursor.close()
        db.close()


def update_user(user_id, name, email):
    db = connect_to_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE users SET name=%s, email=%s WHERE id=%s",
            (name, email, user_id)
        )
        db.commit()
    finally:
        cursor.close()
        db.close()


def delete_user(user_id):
    db = connect_to_db()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        db.commit()
    finally:
        cursor.close()
        db.close()
