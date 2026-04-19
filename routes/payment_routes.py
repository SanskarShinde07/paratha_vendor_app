from flask import Blueprint, request, jsonify
from database.db import get_db_connection

payment_bp = Blueprint("payment_bp", __name__)

@payment_bp.route("/pay", methods=["POST"])
def process_payment():

    data = request.get_json()

    order_id = data.get("order_id")
    payment_method = data.get("payment_method")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE orders SET payment_status=? WHERE order_id=?",
        ("Paid", order_id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Payment successful",
        "order_id": order_id,
        "payment_method": payment_method
    })