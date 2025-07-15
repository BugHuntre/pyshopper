# routes/admin_routes.py
from flask import Blueprint, request, jsonify
from Backend.models import db, User, CartItem, Order, OrderItem
from Backend.utils import save_catalog
from Backend.catalog  import catalog
from Backend.config import ADMIN_EMAIL, ADMIN_PASSWORD
from Services.catalog_service import CatalogService
from Services.order_service import OrderService
from Services.user_service import UserService

admin_bp = Blueprint('admin', __name__)

def is_admin(email, password):
    return email == ADMIN_EMAIL and password == ADMIN_PASSWORD

@admin_bp.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.json
    if is_admin(data.get("email"), data.get("password")):
        return jsonify({"message": "Admin login successful", "name": "Admin"}), 200
    return jsonify({"error": "Invalid admin credentials"}), 401

@admin_bp.route("/admin/catalog/add", methods=["POST"])
def admin_add_catalog_item():
    data = request.json
    if not is_admin(data.get("email"), data.get("password")):
        return jsonify({"error": "Unauthorized"}), 403

    item = data.get("item")
    if not item or not item.get("name") or not item.get("price"):
        return jsonify({"error": "Missing item name or price"}), 400

    if any(existing["name"].lower() == item["name"].lower() for existing in catalog):
        return jsonify({"error": "Item already exists"}), 409

    catalog.append(item)
    save_catalog(catalog)
    return jsonify({"message": f"{item['name']} added to catalog"}), 201

@admin_bp.route("/admin/users/", methods=["POST"])
def get_all_users():
    data = request.json
    if not is_admin(data.get("email"), data.get("password")):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        all_users = User.query.all()
        users_data = [{"email": u.email, "name": u.name} for u in all_users]
        return jsonify({"users": users_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/admin/users/<email>", methods=["GET"])
def get_user_details(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart_items = CartItem.query.filter_by(user_email=email).all()
    orders = Order.query.filter_by(user_email=email).all()

    user_cart = [
        {"name": item.product_name, "price": item.price, "quantity": item.quantity}
        for item in cart_items
    ]

    user_orders = []
    for order in orders:
        items = OrderItem.query.filter_by(order_id=order.id).all()
        user_orders.append({
            "id": order.id,
            "timestamp": order.timestamp,
            "total": order.total_amount,
            "items": [
                {"name": i.product_name, "price": i.price, "quantity": i.quantity}
                for i in items
            ]
        })

    return jsonify({"cart": user_cart, "orders": user_orders}), 200
