"""Run with the .venv Python executable; no external test framework is needed."""

# Use the standard library test runner; no additional testing framework is required.
import unittest

# Match Jinja's HTML escaping when comparing product text with rendered HTML.
from markupsafe import escape

# Import the real application and catalog so requests exercise the actual route.
from app import app, products
from models.product import DigitalProduct, PhysicalProduct, Product


# Group automated checks; unittest discovers methods whose names start with test_.
class ShowcaseChecks(unittest.TestCase):
    # Check every available category, including both included and excluded product titles.
    def test_category_filter(self):
        # Send requests directly to Flask without starting a browser or network server.
        with app.test_client() as client:
            for category in {product.category for product in products}:
                # Report the category responsible for a failure while continuing other cases.
                with self.subTest(category=category):
                    response = client.get(
                        "/",
                        # Encode the selected category as URL query parameters, including any spaces.
                        query_string={"category": category},
                    )
                    self.assertEqual(response.status_code, 200)
                    # Decode the response body into text so assertions can inspect the rendered HTML.
                    html = response.get_data(as_text=True)

                    # Compute the expected matching objects independently of the route response.
                    expected = [
                        product
                        for product in products
                        if product.category == category
                    ]

                    self.assertEqual(
                        html.count('<article class="card">'),
                        len(expected),
                    )

                    for product in products:
                        # Look for a card title rather than a name that could appear elsewhere on the page.
                        title = f"<h3>{escape(product.name)}</h3>"

                        if product.category == category:
                            self.assertIn(title, html)
                        else:
                            self.assertNotIn(title, html)

    # Check that an unmatched category returns a successful page with no product cards.
    def test_unknown_category(self):
        existing_categories = {product.category for product in products}
        unknown_category = "Unknown"

        # Ensure the test input stays unknown even if the catalog later gains more categories.
        while unknown_category in existing_categories:
            unknown_category += "_"

        response = app.test_client().get(
            "/",
            query_string={"category": unknown_category},
        )
        self.assertEqual(response.status_code, 200)
        # Decode the response body into text so assertions can inspect the rendered HTML.
        html = response.get_data(as_text=True)
        self.assertEqual(html.count('<article class="card">'), 0)

    # Check the unfiltered page, its card count, displayed product data, and image URLs.
    def test_page_and_content(self):
        response = app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        # Decode the response body into text so assertions can inspect the rendered HTML.
        html = response.get_data(as_text=True)
        self.assertIn('<html lang="en">', html)
        self.assertEqual(html.count('<article class="card">'), len(products))
        for product in products:
            # Match Jinja's automatic HTML escaping.
            for text in (product.name, product.formatted_price(), product.delivery()):
                self.assertIn(str(escape(text)), html)
            self.assertIn(f'/static/images/{product.image}', html)

    # Check that the stylesheet and starter image can be served with the expected MIME types.
    def test_static_files(self):
        # Send requests directly to Flask without starting a browser or network server.
        with app.test_client() as client:
            for path, mime_type in (
                ("/static/css/style.css", "text/css"),
                ("/static/images/placeholder.svg", "image/svg+xml"),
            ):
                response = client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.mimetype, mime_type)
                self.assertTrue(response.data)
                if path.endswith(".svg"):
                    self.assertIn("Your photo here", response.get_data(as_text=True))
                # Release the resources associated with the static file response.
                response.close()

    # Verify that the abstract Product class cannot be instantiated directly.
    def test_abstraction(self):
        with self.assertRaises(TypeError):
            Product(name="Test", description="Test", price=1, image="placeholder.svg")

    # Exercise both concrete classes, constructor validation, later assignments, and price formatting.
    def test_models(self):
        for product_class, extra in (
            (PhysicalProduct, {"pickup_location": "Library"}),
            (DigitalProduct, {"file_format": "PDF"}),
        ):
            with self.subTest(product_class=product_class.__name__):
                arguments = dict(name="Test", description="Test", image="placeholder.svg", category="Test", product_id="test-product", **extra)
                with self.assertRaisesRegex(ValueError, "The price cannot be negative."):
                    # Expand the argument dictionary and verify that a negative initial price is rejected.
                    product_class(price=-1, **arguments)
                product = product_class(price=59.90, **arguments)
                self.assertIsInstance(product, Product)
                self.assertEqual(product.formatted_price(), "R$ 59,90")
                with self.assertRaisesRegex(ValueError, "The price cannot be negative."):
                    # Verify that later assignments also pass through the same validating setter.
                    product.price = -1
                self.assertEqual(product.price, 59.90)
                # Verify the boundary case: a zero price is accepted and formatted with two decimals.
                product.price = 0
                self.assertEqual(product.formatted_price(), "R$ 0,00")
                product.price = 12.50
                self.assertEqual(product.formatted_price(), "R$ 12,50")

    # Verify that both product types expose delivery() but return their own delivery information.
    def test_polymorphism(self):
        physical = PhysicalProduct(
            name="Test", description="Test", price=1,
            image="placeholder.svg", pickup_location="Library", category="Test",product_id="test-digital",
        )
        digital = DigitalProduct(
            name="Test", description="Test", price=1,
            image="placeholder.svg", file_format="PDF", category="Test",product_id="test-digital",
        )
        self.assertNotEqual(physical.delivery(), digital.delivery())
        self.assertIn("Library", physical.delivery())
        self.assertIn("PDF", digital.delivery())


# Run the test suite only when this file is executed directly, not when imported.
if __name__ == "__main__":
    # Print each test name and its outcome, followed by the suite summary.
    unittest.main(verbosity=2)
