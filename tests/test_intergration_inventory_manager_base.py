import unittest
from inventory_manager import app, products, categories

class InventoryManagerIntegrationTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Initialize products and categories for each test
        global products, categories
        products.clear()
        products.extend([
            {"id": 1, "name": "Laptop", "price": 1200, "quantity": 10, "category": "Electronics"},
            {"id": 2, "name": "Mouse", "price": 25, "quantity": 100, "category": "Accessories"}
        ])
        categories.clear()
        categories.extend([
            {"id": 1, "name": "Electronics"},
            {"id": 2, "name": "Accessories"}
        ])

    def test_add_product_and_verify(self):
        """Test adding a product and verifying its existence on the main page."""
        # Add a new product
        response = self.app.post('/add_product', data={
            "name": "Keyboard",
            "price": 50,
            "quantity": 20,
            "category": "Accessories"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Keyboard', response.data)

        # Verify that the product was added
        response_get = self.app.get('/')
        self.assertIn(b'Keyboard', response_get.data)
        self.assertIn(b'50', response_get.data)
        self.assertIn(b'20', response_get.data)
        self.assertIn(b'Accessories', response_get.data)

    def test_delete_product_and_verify(self):
        """Test deleting a product and verifying its removal."""
        # Delete the first product (Laptop)
        response = self.app.post('/delete_product/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Laptop', response.data)

        # Verify that the product is no longer on the main page
        response_get = self.app.get('/')
        self.assertNotIn(b'Laptop', response_get.data)

    def test_add_category_and_verify(self):
        """Test adding a category and verifying its existence on the main page."""
        # Add a new category
        response = self.app.post('/add_category', data={"name": "Gaming"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gaming', response.data)

        # Verify that the category was added
        response_get = self.app.get('/')
        self.assertIn(b'Gaming', response_get.data)

    def test_combined_product_and_category_operations(self):
        """Test adding a category, then adding a product in that category, and verifying both."""
        # Add a new category
        self.app.post('/add_category', data={"name": "Gaming"}, follow_redirects=True)

        # Add a new product in the 'Gaming' category
        response = self.app.post('/add_product', data={
            "name": "Gaming Mouse",
            "price": 80,
            "quantity": 15,
            "category": "Gaming"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gaming Mouse', response.data)

        # Verify that both the product and category are displayed correctly
        response_get = self.app.get('/')
        self.assertIn(b'Gaming Mouse', response_get.data)
        self.assertIn(b'80', response_get.data)
        self.assertIn(b'15', response_get.data)
        self.assertIn(b'Gaming', response_get.data)


if __name__ == '__main__':
    unittest.main()
