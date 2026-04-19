from flask import Blueprint, jsonify
from database.db import get_db_connection

menu_bp = Blueprint("menu_bp", __name__)

@menu_bp.route("/menu", methods=["GET"])
def get_menu():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM menu_items")
    items = cursor.fetchall()

    conn.close()

    menu = []

    for item in items:
        menu.append({
            "item_id": item["item_id"],
            "name": item["name"],
            "price": item["price"]
        })

    return jsonify(menu)