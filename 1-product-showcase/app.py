from flask import Flask, render_template

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
        price=99.90,
        image="minecraft.jfif",
        pickup_location="One More Level pickup point",
    ),
    PhysicalProduct(
        name="The Witcher 3: Wild Hunt",
        description="Become Geralt of Rivia, a monster hunter for hire, and explore a vast open world filled with dangerous creatures, powerful choices, and unforgettable stories.",
        price=79.90,
        image="thewitcher3.jpg",
        pickup_location="One More Level pickup point",
    ),
    DigitalProduct(
    name="Crimson Desert",
    description="Explore the vast continent of Pywel as Kliff, facing fierce enemies and discovering a world filled with adventure.",
    price=249.90,
    image="Crimson-Desert.jpg",
    file_format="Midia digital",
),
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        showcase_name=SHOWCASE_NAME,
        showcase_description=SHOWCASE_DESCRIPTION,
        author_name=AUTHOR_NAME,
        products=products,
    )
