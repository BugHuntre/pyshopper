import json
from app import app, db
from Backend.models import Product  # adjust if needed

# Load catalog.json data
with open('catalog.json', 'r') as f:
    catalog_data = json.load(f)

with app.app_context():
    for item in catalog_data:
        name = item.get("name", "Unnamed")
        price = float(item.get("price", 0))
        quantity = int(item.get("quantity", 0))
        item_type = item.get("type", "generic").lower()

        shipping_weight = float(item.get("shipping_weight", 0)) if item_type == "physical" else None
        file_size_mb = float(item.get("file_size_mb", 0)) if item_type == "digital" else None

        product = Product(
            name=name,
            price=price,
            quantity=quantity,
            type=item_type,
            shipping_weight=shipping_weight,
            file_size_mb=file_size_mb
        )

        db.session.add(product)

    db.session.commit()
    print("✅ Catalog seeded successfully.")
