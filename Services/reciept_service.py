# services/receipt_service.py
import os
import datetime
from config import BASE_DIR

RECEIPT_DIR = os.path.join(BASE_DIR, "receipts")
os.makedirs(RECEIPT_DIR, exist_ok=True)

class ReceiptService:
    @staticmethod
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
