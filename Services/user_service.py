# services/user_service.py
import json
from config import USERS_FILE
from user import UserAccount
from cart import Cart

class UserService:
    @staticmethod
    def save_users_to_file(users, filename=USERS_FILE):
        data = {
            email: {
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "cart": user.cart.to_dict(),
                "wishlist": user.wishlist.to_dict(),
                "orders": user.orders
            }
            for email, user in users.items()
        }
        with open(filename, "w") as file:
            json.dump(data, file)
        print("Users and carts saved to file.")

    @staticmethod
    def load_users_from_file(filename=USERS_FILE):
        users = {}
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for email, info in data.items():
                    user = UserAccount(info["name"], info["email"], info["password"])
                    user.cart = Cart.from_dict(info.get("cart", []))
                    user.wishlist = Cart.from_dict(info.get("wishlist", []))
                    user.orders = info.get("orders", [])
                    users[email] = user
            print("Users loaded from file.")
        except FileNotFoundError:
            print("No saved users found. Starting fresh.")
        except json.JSONDecodeError:
            print("⚠️ Corrupted users.json. Starting fresh.")
        return users
