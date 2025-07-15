# routes/checkout_routes.py

from flask import Blueprint, request, jsonify, send_from_directory
from datetime import datetime
import os
from models import db, CartItem, Order, OrderItem
from config import BASE_DIR
from Services.reciept_service import ReceiptService
from Services.order_service import OrderService

checkout_bp = Blueprint("checkout", __name__)
RECEIPT_DIR = os.path.join(BASE_DIR, "receipts")
os.makedirs(RECEIPT_DIR, exist_ok=True)


@checkout_bp.route("/cart/checkout", methods=["POST"])
def checkout_cart():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Missing email"}), 400

    cart_items = CartItem.query.filter_by(user_email=email).all()
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    try:
        # Step 0: Cache item data into plain list BEFORE deletion
        item_list = [
            {
                "name": item.product_name,
                "price": item.price,
                "quantity": item.quantity
            }
            for item in cart_items
        ]

        total = sum(item["price"] * item["quantity"] for item in item_list)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Step 1: Generate receipt text
        lines = [
            "🧾 PyShopper Receipt",
            f"👤 Email: {email}",
            f"📅 Date: {timestamp}",
            "-" * 40
        ]
        for item in item_list:
            lines.append(f"{item['name']} - ₹{item['price']} × {item['quantity']}")
        lines.append("-" * 40)
        lines.append(f"🧮 Total: ₹{total}")
        receipt_text = "\n".join(lines)

        # Step 2: Create Order
        order = Order(user_email=email, timestamp=timestamp, total_amount=total, receipt_file="")
        db.session.add(order)
        db.session.commit()

        # Step 3: Create OrderItems
        for item in item_list:
            db.session.add(OrderItem(
                order_id=order.id,
                product_name=item["name"],
                price=item["price"],
                quantity=item["quantity"]
            ))
        db.session.commit()

        # Step 4: Save receipt file
        safe_email = email.replace("@", "_at_").replace(".", "_")
        filename = f"receipt_{safe_email}_{order.id}.txt"
        filepath = os.path.join(RECEIPT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(receipt_text)

        # Step 5: Update order with receipt filename
        order.receipt_file = filename
        db.session.commit()

        # Step 6: Clear cart
        db.session.query(CartItem).filter_by(user_email=email).delete()
        db.session.commit()

        return jsonify({
            "message": "Order confirmed!",
            "receipt_preview": receipt_text,
            "receipt_file": filename,
            "order_id": order.id
        }), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Checkout failed: {str(e)}"}), 500


@checkout_bp.route("/receipts/<filename>", methods=["GET"])
def download_receipt(filename):
    return send_from_directory(RECEIPT_DIR, filename, as_attachment=True)
