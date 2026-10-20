# Import the web application class and the function that renders Jinja templates.
#from flask import Flask, render_template
# request exposes the current HTTP request, including URL query parameters.
#from flask import Flask, render_template, request
import os

from flask import Flask, render_template, request, session, redirect, url_for

# Import the local product types used to build the in-memory catalog.
from models.product import DigitalProduct, PhysicalProduct

# Create the Flask application; the module name helps Flask locate templates and static files.
app = Flask(__name__)
# CUSTOMIZE HERE: choose a theme and introduce your showcase.
# Read the session signing key from the environment.
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
SHOWCASE_NAME = "One More Level"
SHOWCASE_DESCRIPTION = "Your next adventure starts here."
AUTHOR_NAME = "Gilvalter Sales"

# CUSTOMIZE HERE: prices are numbers with a decimal point, without R$.
# Keep product objects in memory. These demonstration prices are not live store prices.
products = [
    PhysicalProduct(
        name="Minecraft",
        description="Build, explore, and create your own adventure.",
        price=99.99,
        image="minecraft.jfif",
        pickup_location="One More Level pickup point",
        category="Sandbox",
        product_id="minecraft",
    ),
    PhysicalProduct(
        name="The Witcher 3: Wild Hunt",
        description="Become Geralt of Rivia, a monster hunter for hire, and explore a vast open world filled with dangerous creatures, powerful choices, and unforgettable stories.",
        price=79.90,
        image="thewitcher3.jpg",
        pickup_location="One More Level pickup point",
        category="RPG",
        product_id="the-witcher-3"
    ),
    DigitalProduct(
        name="Crimson Desert",
        description="Explore the vast continent of Pywel as Kliff, facing fierce enemies and discovering a world filled with adventure.",
        price=249.90,
        image="Crimson-Desert.jpg",
        file_format="Midia digital",
        category="Action Adventure",
        product_id="crimson-desert"
    ),
]
def get_product_by_id(product_id):
    # Find the catalog product with the requested identifier.
    for product in products:
        if product.product_id == product_id:
            return product

    return None

# Associate the home URL with index; the default route accepts GET requests.
@app.route("/")
def index():
    # Read ?category=... from the URL; an absent parameter becomes an empty string.
    selected_category = request.args.get("category", "")
    # Start with the full catalog. This assignment references the list rather than copying it.
    filtered_products = products

    # Only filter when a nonempty category was supplied; comparisons are case-sensitive.
    if selected_category:
        # Build a new list containing only objects whose category matches the request.
        filtered_products = [
            product
            for product in products
            if product.category == selected_category
        ]
    # Collect unique categories from the full catalog, then sort them for the selector.
    categories = sorted({product.category for product in products})
    # Render templates/index.html and expose the following named values to Jinja.
    return render_template(
        "index.html",
        showcase_name=SHOWCASE_NAME,
        showcase_description=SHOWCASE_DESCRIPTION,
        author_name=AUTHOR_NAME,
        # Keep the template variable named products while passing the selected subset.
        products=filtered_products,
        categories=categories,
        # Let the template preserve the submitted selection after the page reloads.
        selected_category=selected_category,
    )
@app.route("/cart/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    # Only allow products that exist in the catalog.
    product = get_product_by_id(product_id)
    if product is None:
        return "Product not found.", 404

    # Read the cart, or start with an empty dictionary.
    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + 1

    # Save the updated cart in the session.
    session["cart"] = cart

    return redirect(url_for("index"))
@app.route("/cart")
@app.route("/cart")
def view_cart():
    # Read the cart associated with this browser.
    cart = session.get("cart", {})
    cart_items = []
    total = 0

    # Combine catalog products with their selected quantities.
    for product_id, quantity in cart.items():
        product = get_product_by_id(product_id)

        if product is not None:
            subtotal = product.price * quantity
            total = total + subtotal
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })

    return render_template("cart.html",cart_items=cart_items,total=total,)

@app.route("/cart/remove/<product_id>", methods=["POST"])
def remove_from_cart(product_id):
    # Remove the selected product and all its units.
    cart = session.get("cart", {})
    cart.pop(product_id, None)
    session["cart"] = cart

    return redirect(url_for("view_cart"))
@app.route("/cart/update/<product_id>", methods=["POST"])
def update_cart_quantity(product_id):
    # Read and validate the submitted quantity.
    quantity = request.form.get("quantity", type=int)

    if quantity is None or not 1 <= quantity <= 99:
        return "Quantity must be an integer between 1 and 99.", 400

    # Only update products already present in the cart.
    cart = session.get("cart", {})

    if product_id not in cart:
        return "Product not found in cart.", 404

    cart[product_id] = quantity
    session["cart"] = cart

    return redirect(url_for("view_cart"))