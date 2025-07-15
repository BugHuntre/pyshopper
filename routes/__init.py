from flask import Blueprint

from .auth_routes import auth_bp
from .admin_routes import admin_bp
from .cart_routes import cart_bp
from .wishlist_routes import wishlist_bp
from .checkout_route import checkout_bp
from .orders_routes import order_bp
from .catalog_routes import catalog_bp

def register_all_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(catalog_bp)
