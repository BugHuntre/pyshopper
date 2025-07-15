# services/catalog_service.py
import json
from Backend.config import CATALOG_FILE

class CatalogService:
    @staticmethod
    def load_catalog():
        try:
            with open(CATALOG_FILE, "r") as file:
                print("Product catalog loaded.")
                return json.load(file)
        except FileNotFoundError:
            print("catalog.json not found. No products loaded.")
            return []

    @staticmethod
    def save_catalog(catalog):
        with open(CATALOG_FILE, "w") as f:
            json.dump(catalog, f, indent=2)
