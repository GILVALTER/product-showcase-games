from abc import ABC, abstractmethod


class Product(ABC):
    """Abstraction: share common attributes and require a delivery method."""

    def __init__(self, name, description, price, image, category):
        self.name = name
        self.description = description
        self.price = price  # Construction also goes through validation.
        self.image = image
        self.category = category

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("The price cannot be negative.")
        # _price is internal by convention; the underscore does not block access.
        self._price = value

    def formatted_price(self):
        # Keep the activity's Brazilian real (BRL) display format.
        return f"R$ {self.price:.2f}".replace(".", ",")

    @abstractmethod
    def delivery(self):
        """Each product type must describe its delivery."""


class PhysicalProduct(Product):
    def __init__(self, name, description, price, image, pickup_location, category):
        super().__init__(name, description, price, image, category)
        self.pickup_location = pickup_location

    def delivery(self):
        # CUSTOMIZE HERE: delivery message for a physical product.
        return f"Pickup at: {self.pickup_location}."


class DigitalProduct(Product):
    def __init__(self, name, description, price, image, file_format, category):
        super().__init__(name, description, price, image, category)
        self.file_format = file_format

    def delivery(self):
        # CUSTOMIZE HERE: informational message, without automatic file delivery.
        return f"Digital delivery in {self.file_format} format."
