# test_integration_inventory_manager.py
import unittest
from inventory_manager import app, products

class IntegrationTestInventoryManager(unittest.TestCase):

    # Set up the Flask test client and reset the products list before each test
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        products.clear()  # Clear any leftover data from previous tests
        products.extend([  # Add initial products to ensure consistent state
            {"id": 1, "name": "Laptop", "price": 1200, "quantity": 10, "category": "Electronics"},
            {"id": 2, "name": "Mouse", "price": 25, "quantity": 100, "category": "Accessories"}
        ])
    
    # Integration test: Add a product, retrieve it, update it, and then delete it
    def test_add_retrieve_update_delete_product(self):
        """Test the full product lifecycle: add, retrieve, update, and delete."""

        # Step 1: Add a new product
        response_add = self.app.post('/products', json={
            "name": "Keyboard",
            "price": 50,
            "quantity": 20,
            "category": "Accessories"
        })
        self.assertEqual(response_add.status_code, 201)
        self.assertIn(b'Keyboard', response_add.data)

        # Step 2: Retrieve all products and check if the new product is present
        response_get = self.app.get('/products')
        self.assertEqual(response_get.status_code, 200)
        self.assertIn(b'Keyboard', response_get.data)

        # Step 3: Update the newly added product (assuming it gets ID 3)
        response_update = self.app.put('/products/3', json={
            "price": 60,
            "quantity": 25
        })
        self.assertEqual(response_update.status_code, 200)
        self.assertIn(b'60', response_update.data)
        self.assertIn(b'25', response_update.data)

        # Step 4: Delete the newly added product
        response_delete = self.app.delete('/products/3')
        self.assertEqual(response_delete.status_code, 200)
        self.assertIn(b'Product deleted', response_delete.data)

        # Step 5: Retrieve all products again and ensure the product is gone
        response_get_after_delete = self.app.get('/products')
        self.assertEqual(response_get_after_delete.status_code, 200)
        self.assertNotIn(b'Keyboard', response_get_after_delete.data)

if __name__ == '__main__':
    unittest.main()
