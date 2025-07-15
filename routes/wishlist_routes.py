# routes/wishlist_routes.py

from flask import Blueprint, request, jsonify
from models import db, WishlistItem, CartItem

wishlist_bp = Blueprint("wishlist", __name__)


@wishlist_bp.route('/wishlist/<email>', methods=['GET'])
def get_wishlist(email):
    items = WishlistItem.query.filter_by(user_email=email).all()
    return jsonify({"wishlist": [
        {"name": i.product_name, "price": i.price, "quantity": i.quantity}
        for i in items
    ]})


@wishlist_bp.route("/wishlist/move-to-cart", methods=["POST"])
def move_to_cart():
    data = request.json
    email = data.get("email")
    item_name = data.get("item_name")

    if not email or not item_name:
        return jsonify({"error": "Missing data"}), 400

    wishlist_item = WishlistItem.query.filter_by(user_email=email, product_name=item_name).first()

    if not wishlist_item:
        return jsonify({"error": "Item not found in wishlist"}), 404

    # Check if item already exists in cart
    cart_item = CartItem.query.filter_by(user_email=email, product_name=item_name).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(
            user_email=email,
            product_name=wishlist_item.product_name,
            price=wishlist_item.price,
            quantity=1
        )
        db.session.add(cart_item)

    # Decrease quantity from wishlist
    wishlist_item.quantity -= 1
    if wishlist_item.quantity <= 0:
        db.session.delete(wishlist_item)

    db.session.commit()

    return jsonify({"message": f"1 unit of {item_name} moved to cart."}), 200


@wishlist_bp.route('/wishlist/add', methods=['POST'])
def add_to_wishlist():
    data = request.json
    item = data.get("item")
    email = data.get("email")

    if not email or not item:
        return jsonify({"error": "Missing email or item"}), 400

    db.session.add(WishlistItem(
        user_email=email,
        product_name=item["name"],
        price=float(item["price"]),
        quantity=int(item["quantity"])
    ))
    db.session.commit()
    return jsonify({"message": "Item added to wishlist"}), 200


@wishlist_bp.route("/wishlist/remove", methods=["POST"])
def remove_from_wishlist():
    data = request.json
    item = WishlistItem.query.filter_by(
        user_email=data.get("email"),
        product_name=data.get("item_name")
    ).first()

    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item removed from wishlist"}), 200

    return jsonify({"error": "Item not found"}), 404
