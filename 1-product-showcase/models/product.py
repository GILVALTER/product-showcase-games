# Use Python's built-in abstract class tools to require a delivery implementation.
from abc import ABC, abstractmethod


# Abstraction: define shared product data and behavior without allowing direct instantiation.
class Product(ABC):
    """Abstraction: share common attributes and require a delivery method."""

    def __init__(self, name, description, price, image, category, product_id):
        # Store the received name on this object; each product keeps its own attributes.
        self.name = name
        # Store the descriptive text that Jinja will display inside the card.
        self.description = description
        # Construction also goes through validation.
        self.price = price 
        # Store a filename, not image contents; the template builds its static URL.
        self.image = image
        # Store the category used both for the badge and for server-side filtering.
        self.category = category
         # Store the stable identifier used to find this product.
        self.product_id = product_id
    # Expose price as an attribute while routing reads through the getter below.
    @property
    def price(self):
        # Return the value stored internally after validation.
        return self._price

    # Intercept assignments to price, including assignments made during initialization.
    @price.setter
    def price(self, value):
        # Reject negative numeric prices; zero is valid because the comparison is strictly less than.
        if value < 0:
            # Stop before storing an invalid value and explain the violated business rule.
            raise ValueError("The price cannot be negative.")
        # _price is internal by convention; the underscore does not block access.
        self._price = value

    # Return display text without changing the numeric price stored on the object.
    def formatted_price(self):
        # Keep the activity's Brazilian real (BRL) display format.
        # Format two decimal places, then replace the decimal point with a comma for BRL display.
        return f"R$ {self.price:.2f}".replace(".", ",")

    # Concrete subclasses must implement delivery before their objects can be instantiated.
    @abstractmethod
    def delivery(self):
        """Each product type must describe its delivery."""


# Inheritance: specialize Product with a physical pickup location.
class PhysicalProduct(Product):
    def __init__(self, name, description, price, image, pickup_location, category, product_id):
        # Initialize the shared attributes on this same object, including price validation.
        super().__init__(name, description, price, image, category, product_id)
        # Add the physical-only attribute after initializing the common attributes.
        self.pickup_location = pickup_location

    def delivery(self):
        # CUSTOMIZE HERE: delivery message for a physical product.
        # Polymorphism: provide the physical response to the shared delivery() call.
        return f"Pickup at: {self.pickup_location}."


# Inheritance: specialize Product with a digital file format description.
class DigitalProduct(Product):
    def __init__(self, name, description, price, image, file_format, category, product_id):
        # Initialize the shared attributes on this same object, including price validation.
        super().__init__(name, description, price, image, category, product_id)
        # Add the digital-only attribute; this does not download or deliver a file.
        self.file_format = file_format

    def delivery(self):
        # CUSTOMIZE HERE: informational message, without automatic file delivery.
        # Polymorphism: provide the digital response to the same delivery() call.
        return f"Digital delivery in {self.file_format} format."
