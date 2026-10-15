from flask import Flask, render_template
from flask import Flask, render_template, request

from models.product import DigitalProduct, PhysicalProduct

app = Flask(__name__)

# CUSTOMIZE HERE: choose a theme and introduce your showcase.
SHOWCASE_NAME = "One More Level"
SHOWCASE_DESCRIPTION = "Your next adventure starts here."
AUTHOR_NAME = "Gilvalter Sales"

# CUSTOMIZE HERE: prices are numbers with a decimal point, without R$.
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


@app.route("/")
def index():
    selected_category = request.args.get("category", "")
    filtered_products = products

    if selected_category:
        filtered_products = [
            product
            for product in products
            if product.category == selected_category
        ]
    categories = sorted({product.category for product in products})
    return render_template(
        "index.html",
        showcase_name=SHOWCASE_NAME,
        showcase_description=SHOWCASE_DESCRIPTION,
        author_name=AUTHOR_NAME,
        products=filtered_products,
        categories=categories,
        selected_category=selected_category,
    )