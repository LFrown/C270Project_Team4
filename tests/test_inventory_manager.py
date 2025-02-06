import unittest
from inventory_manager import app, products, categories

class InventoryManagerUITest(unittest.TestCase):

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

    # Test for loading the main page
    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inventory Manager', response.data)
        self.assertIn(b'Laptop', response.data)
        self.assertIn(b'Mouse', response.data)
        self.assertIn(b'Electronics', response.data)
        self.assertIn(b'Accessories', response.data)

    # Test for adding a new product
    def test_add_product(self):
        response = self.app.post('/add_product', data={
            "name": "Keyboard",
            "price": 50,
            "quantity": 20,
            "category": "Accessories"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Keyboard', response.data)

    # Test for deleting a product
    def test_delete_product(self):
        response = self.app.post('/delete_product/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Laptop', response.data)

    # Test for adding a new category
    def test_add_category(self):
        response = self.app.post('/add_category', data={"name": "Gaming"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Gaming', response.data)


if __name__ == '__main__':
    unittest.main()
