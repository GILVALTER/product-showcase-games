# Import the web application class and the function that renders Jinja templates.
from flask import Flask, render_template
# request exposes the current HTTP request, including URL query parameters.
from flask import Flask, render_template, request

# Import the local product types used to build the in-memory catalog.
from models.product import DigitalProduct, PhysicalProduct

# Create the Flask application; the module name helps Flask locate templates and static files.
app = Flask(__name__)

# CUSTOMIZE HERE: choose a theme and introduce your showcase.
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
        
    ),
    PhysicalProduct(
        name="The Witcher 3: Wild Hunt",
        description="Become Geralt of Rivia, a monster hunter for hire, and explore a vast open world filled with dangerous creatures, powerful choices, and unforgettable stories.",
        price=79.90,
        image="thewitcher3.jpg",
        pickup_location="One More Level pickup point",
        category="RPG",
        
    ),
    DigitalProduct(
        name="Crimson Desert",
        description="Explore the vast continent of Pywel as Kliff, facing fierce enemies and discovering a world filled with adventure.",
        price=249.90,
        image="Crimson-Desert.jpg",
        file_format="Midia digital",
         category="Action Adventure",
        
),
]


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
