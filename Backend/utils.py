import json
import os
from Backend.config import USERS_FILE,ORDERS_FILE,CATALOG_FILE
import datetime
import os
from Backend.config import BASE_DIR
RECEIPT_DIR = os.path.join(BASE_DIR, "receipts")
os.makedirs(RECEIPT_DIR, exist_ok=True)

def export_receipt(email, cart_items, total, discount, discount_amount):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"receipt_{email.replace('@','_at_')}_{timestamp}.txt"
    filepath = os.path.join(RECEIPT_DIR, filename)

    with open(filepath, "w") as f:
        f.write(f"Receipt for {email}\n")
        f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 40 + "\n")
        for item in cart_items:
            f.write(f"{item.name} x {item.quantity} @ ₹{item.price} = ₹{item.price * item.quantity}\n")
        f.write("=" * 40 + "\n")
        f.write(f"Subtotal: ₹{total + discount_amount:.2f}\n")
        f.write(f"Discount: {discount}% (-₹{discount_amount:.2f})\n")
        f.write(f"Total: ₹{total:.2f}\n")
    
    return filename

def save_users_to_file(users,filename = USERS_FILE):
    data = {}
    for email,user in users.items():
        data[email] = {
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "cart": user.cart.to_dict(),
            "wishlist": user.wishlist.to_dict(),
            "orders": user.orders
        }
    with open(filename,"w") as file:
        json.dump(data,file)
    print("users and carts saved to file.")

def load_users_from_file(filename=USERS_FILE):
    from Backend.user import UserAccount
    from Backend.cart import Cart
    users = {}

    try:
        with open(filename,"r") as file:
            data = json.load(file)
            for email,user_info in data.items():
                user = UserAccount(
                    
                    user_info["name"],
                    user_info["email"],
                    user_info["password"],

                )
                user.cart = Cart.from_dict(user_info.get("cart",[]))
                user.wishlist = Cart.from_dict(user_info.get("wishlist",[]))
                user.orders = user_info.get("orders",[])
                users[email] = user
        print("Users loaded from file.")
    except FileNotFoundError:
        print("No saved users found. Starting fresh.")
    except json.JSONDecodeError:
        print("⚠️ Corrupted users.json file. Starting with a fresh user list.")

    return users
def load_order_history(filename = ORDERS_FILE):
    try:
        with open(filename,"r") as file:
            return json.load(file)
    except(FileNotFoundError,json.JSONDecodeError):
        return []
def get_valid_integer(prompt, min_value=1):
    while True:
        try:
            value = int(input(prompt))
            if value < min_value:
                print(f"Please enter a number greater than or equal to {min_value}.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
def load_catalog(filename=CATALOG_FILE):
    try:
        with open(filename,"r") as file:
            catalog = json.load(file)
            print("Product catalog loaded.")
            return catalog
    except FileNotFoundError:
        print("catalog.json not found. No products loaded.")
        return []
def save_order_to_history(email,cart,filename = ORDERS_FILE):
    try:
        with open(filename,"r") as file:
            orders = json.load(file)
    except (FileNotFoundError,json.JSONDecodeError):
        orders = []

    order_record = {
            "email": email,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": cart.to_dict()
        }
    orders.append(order_record)
    with open(filename,"w") as file:
            json.dump(orders, file, indent=2)
    print("Order saved to history.")

def save_catalog(catalog):
    with open(CATALOG_FILE, "w") as f:
        json.dump(catalog, f, indent=2)