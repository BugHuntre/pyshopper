# services/input_service.py

class InputService:
    @staticmethod
    def get_valid_integer(prompt, min_value=1):
        while True:
            try:
                value = int(input(prompt))
                if value < min_value:
                    print(f"Enter a number >= {min_value}.")
                else:
                    return value
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
