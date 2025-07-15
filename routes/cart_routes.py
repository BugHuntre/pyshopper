# cart_routes.py
from flask import Flask, Blueprint, request, jsonify , send_from_directory
from Backend.models import db, CartItem
from datetime import datetime
import os
from Backend.models import db,CartItem,Order, OrderItem
from Backend.utils import export_receipt
from Backend.config import RECEIPT_DIR
from Backend.config import BASE_DIR
from flask_cors import CORS
RECEIPT_DIR = os.path.join(BASE_DIR, "receipts")
os.makedirs(RECEIPT_DIR, exist_ok=True)
cart_bp = Blueprint('cart', __name__)
@cart_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.json
    email = data.get("email")
    item = data.get("item")

    if not email or not item:
        return jsonify({"error": "Missing email or item"}), 400

    name = item.get("name")
    price = item.get("price")
    quantity = item.get("quantity")

    if not all([name, price, quantity]):
        return jsonify({"error": "Missing item fields (name, price, quantity)"}), 400

    try:
        new_item = CartItem(
            user_email=email,
            product_name=name,
            price=float(price),
            quantity=int(quantity)
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item added to cart"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add item: {str(e)}"}), 500



@cart_bp.route('/cart/<email>', methods=['GET'])
def get_cart(email):
    items = CartItem.query.filter_by(user_email=email).all()
    return jsonify({
        "cart": [
            {"name": i.product_name, "price": i.price, "quantity": i.quantity}
            for i in items
        ]
    })


@cart_bp.route('/cart/remove-item', methods=['POST'])
def remove_cart_item():
    data = request.json
    item = CartItem.query.filter_by(
        user_email=data.get("email"),
        product_name=data.get("item_name")
    ).first()

    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item removed"}), 200
    return jsonify({"error": "Item not found"}), 404



