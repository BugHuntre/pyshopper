# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECEIPT_DIR = os.path.join(BASE_DIR, "receipts")
USERS_FILE = os.path.join(BASE_DIR, "users.json")
ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")
CATALOG_FILE = os.path.join(BASE_DIR, "catalog.json")
ADMIN_EMAIL = "vishweshpatial@gmail.com"
ADMIN_PASSWORD = "987654321"
RECEIPT_FOLDER = os.path.join(BASE_DIR, "receipts")