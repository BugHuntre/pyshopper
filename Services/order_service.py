# services/order_service.py
import json
import datetime
from config import ORDERS_FILE

class OrderService:
    @staticmethod
    def load_order_history(filename=ORDERS_FILE):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_order_to_history(email, cart, filename=ORDERS_FILE):
        try:
            with open(filename, "r") as file:
                orders = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            orders = []

        orders.append({
            "email": email,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": cart.to_dict()
        })

        with open(filename, "w") as file:
            json.dump(orders, file, indent=2)
        print("Order saved to history.")
