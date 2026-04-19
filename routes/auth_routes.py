from flask import Blueprint, request, jsonify
from database.db import get_db_connection
from utils.security import hash_password, check_password

auth_bp = Blueprint('auth', __name__)

# Register student (for testing)
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    phone = data.get("phone")
    password = data.get("password")

    hashed_pw = hash_password(password)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, phone, password) VALUES (?, ?, ?)",
        (name, phone, hashed_pw)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Registration successful"})

# Login student
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    phone = data.get("phone")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
    "SELECT password FROM users WHERE phone=?",
    (phone,)
)

    user = cursor.fetchone()

    if user and check_password(password, user[0]):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"})