# test_inventory_manager.py
import unittest
from inventory_manager import app, products  # Import 'products' from inventory_manager.py

class InventoryManagerBaseTest(unittest.TestCase):

    # Set up the Flask test client and reset the products list
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Reset the global products list before each test
        products.clear()  # Clear any leftover data from previous tests
        products.extend([  # Add initial products to ensure consistent state
            {"id": 1, "name": "Laptop", "price": 1200, "quantity": 10, "category": "Electronics"},
            {"id": 2, "name": "Mouse", "price": 25, "quantity": 100, "category": "Accessories"}
        ])
        print("SetUp products:", products)

    # Test for retrieving all products
    def test_get_products(self):
        """Ensure that the GET /products route returns all initial products."""
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)  # Check if status code is 200
        self.assertIn(b'Laptop', response.data)  # Check if 'Laptop' is in the response
        self.assertIn(b'Mouse', response.data)  # Check if 'Mouse' is in the response

    # Test for adding a new product
    def test_add_product(self):
        """Ensure that a new product can be added using POST /products."""
        response = self.app.post('/products', json={
            "name": "Keyboard",
            "price": 50,
            "quantity": 20,
            "category": "Accessories"
        })
        self.assertEqual(response.status_code, 201)  # Check if status code is 201 (Created)
        self.assertIn(b'Keyboard', response.data)  # Check if 'Keyboard' is in the response

    # Test for deleting a product
    def test_delete_product(self):
        """Ensure that a product can be deleted using DELETE /products/<id>."""
        response = self.app.delete('/products/1')
        self.assertEqual(response.status_code, 200)  # Check if status code is 200
        self.assertIn(b'Product deleted', response.data)  # Check for success message
        # Verify that the product is no longer in the list
        response_after_delete = self.app.get('/products')
        self.assertNotIn(b'Laptop', response_after_delete.data)

    # Test for updating a product
    def test_update_product(self):
        """Ensure that a product can be updated using PUT /products/<id>."""
        response = self.app.put('/products/2', json={
            "price": 30,
            "quantity": 90
        })
        self.assertEqual(response.status_code, 200)  # Check if status code is 200
        self.assertIn(b'30', response.data)  # Check if '30' is in the updated product
        self.assertIn(b'90', response.data)  # Check if '90' is in the updated product

if __name__ == '__main__':
    unittest.main()
