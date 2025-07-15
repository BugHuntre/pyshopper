from getpass import getpass
from Backend.cart import Cart
from utils import save_users_to_file

class UserAccount:
    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = password
        self.cart = Cart()
        self.wishlist = Cart()
        self.orders = []
    def login(self, max_attempts=3):
        
        attempts = 0

        while attempts < max_attempts:
            pass_input = getpass("Enter your Password: ")

            if pass_input == self.password:
                print(f"Welcome {self.name}! You are logged in.")
                return True
            else:
                print("Incorrect password. Please try again.")
                attempts += 1

        print("Too many failed attempts. Access denied.")
        return False

    def logout(self,users):
        save_users_to_file(users)
        print(f"{self.name}, you have been logged out successfully.")
    def change_password(self):
        
        old_password = getpass("Enter your current password:")
        if old_password == self.password:
            new_password = getpass("Enter you new passsword: ")
            confirm_password = getpass("Confirm your new password: ")

            if new_password == confirm_password:
                self.password = new_password
                print("Password changed successfully.")
            else:
                print("Password does not match. Try again.")
        else:
            print(f"Incorrect current password.")