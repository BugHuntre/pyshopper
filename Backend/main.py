import datetime
import os
import json
from getpass import getpass
from config import USERS_FILE, ORDERS_FILE, CATALOG_FILE, ADMIN_EMAIL, ADMIN_PASSWORD
from items import Item, PhysicalItem, DigitalItem
from cart import Cart
from user import UserAccount
from Backend.utils import (
    save_users_to_file,
    load_users_from_file,
    load_order_history,
    save_order_to_history,
    load_catalog
)



# Load data
orders = load_order_history()
users = load_users_from_file()
catalog = load_catalog()

try:
    while True:
        choice = input("Are you a new user or existing user? (new/existing): ").lower()
        if choice in ("new", "existing"):
            break
        print("Invalid choice. Please enter 'new' or 'existing'.")

    if choice == "new":
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        if email in users:
            print("An account with this email already exists.")
        else:
            password = getpass("Set your password: ")
            users[email] = UserAccount(name, email, password)
            save_users_to_file(users)
            print("Account created and saved successfully!")

    elif choice == "existing":
        email = input("Enter your email: ")

        if email == ADMIN_EMAIL:
            password = getpass("Enter admin password: ")
            if password == ADMIN_PASSWORD:
                while True:
                    print("\n -- Admin Dashboard --")
                    print("1. View all users")
                    print("2. View a user's cart")
                    print("3. Logout")
                    admin_choice = input("Enter your choice (1-3): ")

                    match admin_choice:
                        case "1":
                            print("\n Registered Users:")
                            for user_email, user_obj in users.items():
                                print(f"- {user_obj.name} ({user_email})")
                        case "2":
                            target_email = input("Enter user's email to view their cart: ")
                            if target_email in users:
                                print(f"\nCart for {target_email}:")
                                users[target_email].cart.view_cart()
                            else:
                                print("User not found.")
                        case "3":
                            print("Admin logged out")
                            break
                        case _:
                            print("Invalid choice.")

        elif email in users:
            user = users[email]
            if user.login():
                if user.wishlist.items:
                    print("\nYour Wishlist Items:")
                    for item in user.wishlist.items:
                        print(f"{item.name} x {item.quantity} (${item.price * item.quantity})")
                else:
                    print("\nYour Wishlist is currently empty.")

                while True:
                    print("\n -- Session Menu ---")
                    print("1. View cart")
                    print("2. Add Item Manually")
                    print("3. Add from catalog")
                    print("4. Remove Item")
                    print("5. Checkout")
                    print("6. Apply Discount")
                    print("7. Change Password")
                    print("8. Log out")
                    print("9. Undo Last Action")
                    print("10. View Order History")
                    print("11. Cart Utilities (Sort & Search)")
                    print("12. Wishlist Menu")
                    print("13. Wishlist Utilities")
                    choice = input("Enter your choice (1-13): ")

                    match choice:
                        case "1":
                            user.cart.view_cart()

                        case "2":
                            name = input("Enter item name: ")
                            try:
                                price = float(input("Enter item price: "))
                                if price < 0:
                                    print("Price cannot be negative.")
                                    continue
                                quantity = int(input("Enter quantity: "))
                                item_type = input("Is it (generic/physical/digital)? ").lower()

                                if item_type == "physical":
                                    weight = float(input("Enter shipping weight: "))
                                    item = PhysicalItem(name, price, quantity, weight)
                                elif item_type == "digital":
                                    size = float(input("Enter file size in mb: "))
                                    item = DigitalItem(name, price, quantity, size)
                                else:
                                    item = Item(name, price, quantity)

                                user.cart.add_item(item)
                                save_users_to_file(users)
                            except ValueError:
                                print("Invalid input. Item not added.")

                        case "3":
                            if not catalog:
                                print("Catalog is empty.")
                            else:
                                print("\nAvailable Products:")
                                for i, product in enumerate(catalog, 1):
                                    print(f"{i}. {product['name']} - ${product['price']} ({product['type']})")
                                try:
                                    selection = int(input("Select product number to add: "))
                                    if 1 <= selection <= len(catalog):
                                        prod = catalog[selection - 1]
                                        quantity = int(input("Enter quantity: "))
                                        if prod["type"] == "physical":
                                            item = PhysicalItem(prod["name"], prod["price"], quantity, prod.get("shipping_weight", 0))
                                        elif prod["type"] == "digital":
                                            item = DigitalItem(prod["name"], prod["price"], quantity, prod.get("file_size_in_mb", 0))
                                        else:
                                            item = Item(prod["name"], prod["price"], quantity)
                                        user.cart.add_item(item)
                                        save_users_to_file(users)
                                    else:
                                        print("Invalid product selection.")
                                except ValueError:
                                    print("Please enter a valid number.")

                        case "4":
                            item_name = input("Enter item name to remove: ")
                            user.cart.remove_item(item_name)
                            save_users_to_file(users)

                        case "5":
                            order = user.cart.checkout(email)
                            if order:
                                save_users_to_file(users)

                        case "6":
                            code = input("Enter discount code: ")
                            user.cart.apply_discount(code)
                            save_users_to_file(users)

                        case "7":
                            user.change_password()
                            save_users_to_file(users)

                        case "8":
                            user.logout()
                            break

                        case "9":
                            user.cart.undo_last_action()
                            save_users_to_file(users)

                        case "10":
                            user_orders = [o for o in orders if o["email"] == email]
                            if not user_orders:
                                print("No past orders found.")
                            else:
                                print(f"\n📦 Order History for {email}")
                                for i, order in enumerate(user_orders, 1):
                                    print(f"\n🕒 Order {i} at {order['timestamp']}:")
                                    for item in order["items"]:
                                        print(f"- {item['name']} x {item['quantity']} @ ₹{item['price']}")

                        case "11":
                            while True:
                                print("\nCart Utilities Menu:")
                                print("1. Sort by Price (Low to High)")
                                print("2. Sort by Price (High to Low)")
                                print("3. Filter by Item Type")
                                print("4. Back to Main Menu")
                                sub_choice = input("Enter your choice (1-4): ")

                                match sub_choice:
                                    case "1":
                                        user.cart.sort_items(by="price", reverse=False)
                                    case "2":
                                        user.cart.sort_items(by="price", reverse=True)
                                    case "3":
                                        filter_type = input("Enter type to filter (Generic/Physical/Digital): ")
                                        user.cart.filter_items_by_type(filter_type)
                                    case "4":
                                        break
                                    case _:
                                        print("Invalid choice. Try again.")

                        case "12":
                            while True:
                                print("\n-- Wishlist Menu --")
                                print("a. View Wishlist")
                                print("b. Add item to Wishlist")
                                print("c. Remove Item from Wishlist")
                                print("d. Move Item to Cart")
                                print("e. Add from catalog to Wishlist")
                                print("f. Return to main menu")
                                wishlist_choice = input("Select an option (a-f): ").lower()

                                match wishlist_choice:
                                    case "a":
                                        user.wishlist.view_cart()
                                    case "b":
                                        name = input("Enter item name: ")
                                        try:
                                            price = float(input("Enter item price: "))
                                            quantity = int(input("Enter quantity: "))
                                            item_type = input("Is it (generic/physical/digital)? ").lower()

                                            if item_type == "physical":
                                                weight = float(input("Enter item's shipping weight: "))
                                                item = PhysicalItem(name, price, quantity, weight)
                                            elif item_type == "digital":
                                                size = float(input("Enter file size in mb: "))
                                                item = DigitalItem(name, price, quantity, size)
                                            else:
                                                item = Item(name, price, quantity)

                                            user.wishlist.add_item(item)
                                            save_users_to_file(users)
                                        except ValueError:
                                            print("Invalid input. Item not added.")
                                    case "c":
                                        name = input("Enter the item's name to remove: ")
                                        user.wishlist.remove_item(name)
                                        save_users_to_file(users)
                                    case "d":
                                        name = input("Enter item name to move to cart: ")
                                        found = False
                                        for item in user.wishlist.items:
                                            if item.name.lower() == name.lower():
                                                user.cart.add_item(item)
                                                user.wishlist.remove_item(name)
                                                print("Moved from wishlist to cart.")
                                                save_users_to_file(users)
                                                found = True
                                                break
                                        if not found:
                                            print("Item not found in wishlist.")
                                    case "e":
                                        if not catalog:
                                            print("Catalog is empty.")
                                        else:
                                            print("\nAvailable Products:")
                                            for i, product in enumerate(catalog, 1):
                                                print(f"{i}. {product['name']} - ${product['price']} ({product['type']})")
                                            try:
                                                selection = int(input("Select product number to add to wishlist: "))
                                                if 1 <= selection <= len(catalog):
                                                    prod = catalog[selection - 1]
                                                    quantity = int(input("Enter quantity: "))
                                                    if prod["type"] == "physical":
                                                        item = PhysicalItem(prod["name"], prod["price"], quantity, prod.get("shipping_weight", 0))
                                                    elif prod["type"] == "digital":
                                                        item = DigitalItem(prod["name"], prod["price"], quantity, prod.get("file_size_in_mb", 0))
                                                    else:
                                                        item = Item(prod["name"], prod["price"], quantity)
                                                    user.wishlist.add_item(item)
                                                    save_users_to_file(users)
                                                else:
                                                    print("Invalid product selection.")
                                            except ValueError:
                                                print("Please enter a valid number.")
                                    case "f":
                                        break
                                    case _:
                                        print("Invalid choice. Try again.")

                        case "13":
                            print("Wishlist utilities not yet implemented.")

                        case _:
                            print("Invalid choice. Please try again.")

        else:
            print("No account found with this email.")

except KeyboardInterrupt:
    print("\nDetected Ctrl+C - exiting session gracefully...")

finally:
    save_users_to_file(users)
    print("Session data auto-saved. Goodbye!")
