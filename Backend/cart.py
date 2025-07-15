from items import Item,DigitalItem,PhysicalItem
import datetime
import os
from Backend.utils import save_order_to_history
from Backend.config import BASE_DIR
class Cart:
    def __init__(self):
        self.items = []
        self.discount = 0
        self.action_stack = [] # for undo functionality
    def add_item(self, item):
        if item.quantity <= 0 or item.price < 0:
            print("Invalid item quantity or price.")
            return

        for existing_item in self.items:
            if (
                existing_item.name.lower() == item.name.lower()
                and existing_item.get_type() == item.get_type()
            ):
                existing_item.quantity += item.quantity
                print(f"Added {item.quantity} more of {item.name}.")
                return

        self.items.append(item)
        self.action_stack.append(("add", item))
        print(f"{item.name} added to cart.")


    def remove_item(self,item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                removed_item = Item(item.name, item.price,1)
                self.action_stack.append(("remove",removed_item))
                item.quantity -= 1
                if item.quantity <= 0:
                    self.items.remove(item)
                    print(f"{item.name} remove from the cart.")
                else:
                    print(f"One {item.name} removed. Remaining: {item.quantity}")
                return
        print(f"{item_name} not found in cart.")
    def view_cart(self):
        if not self.items:
            print("Cart is empty")
        else:
            print("Items in cart: ")
            for item in self.items:
                print(f"{item.name} x {item.quantity} : ${item.price * item.quantity}")
    def total_price(self):
        total = sum(item.price * item.quantity for item in self.items)
        if self.discount > 0:
            total -= total * (self.discount/100)
            print(f"Discount applied: {self.discount}%")
        print(f"Total price: ${total}")
        return total
    def apply_discount(self,code):
        if code == "SAVE10":
            self.discount = 10
            print("Discount of 10% applied!")
        elif code == "SAVE20":
            self.discount = 20
            print("Discount of 20% applied")
        else:
            print("Invalid discount code")
    def generate_receipt(self,return_as_string = False):
        lines = []
        lines.append("\n Reciept:")
        lines.append("-"* 50)
        lines.append(f"{'Item': <15}{'Qty':<5}{'price':<10}{'Subtotal'}")
        lines.append("-" * 50)

        total = 0
        for item in self.items:
            subtotal = item.price * item.quantity
            total += subtotal
            lines.append(f"{item.name} ({item.get_type()}) x {item.quantity:<5} = ${subtotal:.2f}")

        lines.append("-"*50)
        lines.append(f"{'Total':<35}${total:.2f}")
        if self.discount > 0:
            discount_amount = total * (self.discount/100)
            final_amount = total - discount_amount
            lines.append(f"{'Discount Applied(' + str(self.discount) + '%)':<35}-${discount_amount:.2f}")
            lines.append(f"{'Final Amount':<35}${final_amount:.2f}")
        else:
            lines.append(f"{'Final Amount':<35}${total}")
        lines.append("-" * 50)
        receipt_text = "\n".join(lines)

        if return_as_string:
            return receipt_text
        else:
            print(receipt_text)
    def checkout(self, email):
        if not self.items:
            print("Your cart is empty")
            return []
        self.generate_receipt()
        confirm = input("Do you want to confirm your order ? (yes/no): ").lower()
        if confirm == "yes":
            order_data = self.to_dict()
            save_order_to_history(email, self)
            #Export reciept to a file 
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_email = email.replace("@","_at_").replace(".","_")
            reciept_filename = f"receipt_{safe_email}_{timestamp}.txt"
            reciept_dir = os.path.join(BASE_DIR,"reciepts")
            os.makedirs(reciept_dir,exist_ok = True)
            reciept_path = os.path.join(reciept_dir,reciept_filename)
            with open(reciept_path,"w") as f:
                f.write(self.generate_receipt(return_as_string= True))
            self.items.clear()
            print(f"Reciept savved to {reciept_path}")
            print("Order confirmed! Thank you for shopping.")
            return order_data
        else:
            print("Order cancelled")
            return []
    def to_dict(self):
        return [
            {
                "type": item.get_type(),
                "name": item.name,
                "price": item.price,
                "quantity": item.quantity,
                "shipping_weight": getattr(item, "shipping_weight", None),
                "file_size_mb": getattr(item, "file_size_mb", None)
            }
            for item in self.items
    ]
    @classmethod
    def from_dict(cls, item_list):
        cart = cls()
        for data in item_list:
            item_type = data.get("type","Generic")
            if item_type == "Physical":
                item = PhysicalItem(data["name"],data["price"],data["quantity"],data.get("shipping_weight",0))
            elif item_type == "Digital":
                item = DigitalItem(data["name"],data["price"],data["quantity"],data.get("file_size_mb",0))
            else:
                item = Item(data["name"],data["price"],data["quantity"])
            cart.items.append(item)
        return cart
    def undo_last_action(self):
        if not self.action_stack:
            print("No action to undo.")
            return
        action,item = self.action_stack.pop()

        if action == "add":
            self.remove_item(item.name)
            print("Removed recently added {item.name}")
        elif action == "remove":
            self.add_item(item)
            print(f"Undo: Re-added recently removed {item.name}")
    def sort_items(self,by="price",reverse = False):
        if not self.items:
            print("Cart is empty")
            return
        if by == "price":
            self.items.sort(key= lambda item:item.price, reverse = reverse)
            print("Items sorts by price (descending.)" if reverse else "Item sorted by price (ascending).")
            self.view_cart()
    def filter_items_by_type(self, item_type):
        filtered = [item for item in self.items if item.get_type().lower() == item_type.lower()]
        if not filtered:
            print(f"No {item_type} items found in the cart.")
        else:
            print(f"{item_type.title()} Items in Cart:")
            for item in filtered:
                print(f"{item.name} x {item.quantity} = ${item.price * item.quantity}")