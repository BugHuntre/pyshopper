# routes/catalog_routes.py

from flask import Blueprint, jsonify
from models import Product
from Services.catalog_service import CatalogService

catalog_bp = Blueprint("catalog", __name__)


@catalog_bp.route("/catalog", methods=["GET"])
def get_catalog():
    products = Product.query.all()
    return jsonify([{
        "name": p.name,
        "price": p.price,
        "quantity": p.quantity,
        "type": p.type,
        "shipping_weight": p.shipping_weight if p.type == "physical" else None,
        "file_size_mb": p.file_size_mb if p.type == "digital" else None
    } for p in products])
