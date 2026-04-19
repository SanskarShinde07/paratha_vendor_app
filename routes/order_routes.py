from flask import Blueprint, request, jsonify
from database.db import get_db_connection

order_bp = Blueprint("orders", __name__)


# =========================
# PLACE ORDER (USER)
# =========================
@order_bp.route("/place_order", methods=["POST"])
def place_order():

    data = request.get_json()

    student_id = data.get("student_id")
    items = data.get("items")

    conn = get_db_connection()
    cursor = conn.cursor()

    total_price = 0

    for item in items:
        item_id = item["item_id"]
        quantity = item["quantity"]

        cursor.execute(
            "SELECT price FROM menu_items WHERE item_id=?",
            (item_id,)
        )

        price = cursor.fetchone()["price"]
        total_price += price * quantity

    # Default status changed to "Preparing" (better for admin flow)
    cursor.execute(
        "INSERT INTO orders (student_id,total_price,status) VALUES (?,?,?)",
        (student_id, total_price, "Preparing")
    )

    order_id = cursor.lastrowid

    for item in items:
        item_id = item["item_id"]
        quantity = item["quantity"]

        cursor.execute(
            "INSERT INTO order_items (order_id,item_id,quantity) VALUES (?,?,?)",
            (order_id, item_id, quantity)
        )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Order placed successfully",
        "order_id": order_id,
        "total_price": total_price
    })


# =========================
# USER ORDERS
# =========================
@order_bp.route("/orders/<student_id>", methods=["GET"])
def get_orders(student_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT order_id, total_price, status FROM orders WHERE student_id=?",
        (student_id,)
    )

    rows = cursor.fetchall()

    orders = []

    for row in rows:
        orders.append({
            "order_id": row["order_id"],
            "total_price": row["total_price"],
            "status": row["status"]
        })

    conn.close()

    return jsonify(orders)


# =========================
# ADMIN - ALL ORDERS
# =========================
@order_bp.route("/vendor/orders", methods=["GET"])
def vendor_orders():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT order_id, student_id, total_price, status, payment_status FROM orders ORDER BY order_id DESC"
    )

    rows = cursor.fetchall()

    orders = []

    for row in rows:
        orders.append({
            "order_id": row["order_id"],
            "student_id": row["student_id"],
            "total_price": row["total_price"],
            "status": row["status"],
            "payment_status": row["payment_status"]
        })

    conn.close()

    return jsonify(orders)


# =========================
# ADMIN - UPDATE STATUS
# =========================
@order_bp.route("/vendor/update_status", methods=["POST"])
def update_order_status():

    data = request.get_json()

    order_id = data.get("order_id")
    status = data.get("status")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE orders SET status=? WHERE order_id=?",
        (status, order_id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Order status updated successfully"
    })


# =========================
# ADMIN - ORDER DETAILS
# =========================
@order_bp.route("/vendor/order_details/<int:order_id>", methods=["GET"])
def order_details(order_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT menu_items.name, order_items.quantity
        FROM order_items
        JOIN menu_items ON order_items.item_id = menu_items.item_id
        WHERE order_items.order_id = ?
    """, (order_id,))

    rows = cursor.fetchall()

    items = []

    for row in rows:
        items.append({
            "item_name": row["name"],
            "quantity": row["quantity"]
        })

    conn.close()

    return jsonify(items)