class Item:
    def __init__(self, name, price, quantity=1):
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_type(self):
        return "Generic"

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "type": self.get_type()
        }


class PhysicalItem(Item):
    def __init__(self, name, price, quantity=1, shipping_weight=0):
        super().__init__(name, price, quantity)
        self.shipping_weight = shipping_weight

    def get_type(self):
        return "Physical"

    def to_dict(self):
        data = super().to_dict()
        data["shipping_weight"] = self.shipping_weight
        return data


class DigitalItem(Item):
    def __init__(self, name, price, quantity=1, file_size_mb=0):
        super().__init__(name, price, quantity)
        self.file_size_mb = file_size_mb

    def get_type(self):
        return "Digital"

    def to_dict(self):
        data = super().to_dict()
        data["file_size_mb"] = self.file_size_mb
        return data
