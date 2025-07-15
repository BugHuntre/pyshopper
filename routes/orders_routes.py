from flask import Blueprint, jsonify
from Backend.models import Order, OrderItem
from Services.order_service import OrderService

order_bp = Blueprint("order", __name__)


@order_bp.route("/orders/<email>", methods=["GET"])
def get_order_history(email):
    try:
        user_orders = Order.query.filter_by(user_email=email).order_by(Order.id.desc()).all()
        result = []
        for order in user_orders:
            items = OrderItem.query.filter_by(order_id=order.id).all()
            result.append({
                "id": order.id,
                "timestamp": order.timestamp,
                "total": order.total_amount,
                "receipt_file": order.receipt_file,
                "items": [
                    {
                        "name": item.product_name,
                        "price": item.price,
                        "quantity": item.quantity
                    } for item in items
                ]
            })
        return jsonify({"orders": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
