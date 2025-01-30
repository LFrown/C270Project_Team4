from pyats import aetest
import requests

# Define API Base URL
BASE_URL = "http://127.0.0.1:5000"  # Adjust if using a different host

class CommonSetup(aetest.CommonSetup):
    """Setup test environment."""

    @aetest.subsection
    def check_server_status(self):
        """Verify if the API server is running before testing."""
        try:
            response = requests.get(f"{BASE_URL}/products")
            if response.status_code == 200:
                self.passed("API server is reachable.")
            else:
                self.failed("API server is not reachable.")
        except requests.exceptions.ConnectionError:
            self.failed("API server is not running. Start Flask first!")

class TestInventoryAPI(aetest.Testcase):
    """Test case for Inventory Manager API."""

    @aetest.test
    def test_get_products(self):
        """Test retrieving all products."""
        response = requests.get(f"{BASE_URL}/products")
        if response.status_code == 200 and "Laptop" in response.text:
            self.passed("GET /products passed.")
        else:
            self.failed(f"GET /products failed. Response: {response.text}")

    @aetest.test
    def test_add_product(self):
        """Test adding a new product."""
        payload = {
            "name": "Keyboard",
            "price": 50,
            "quantity": 20,
            "category": "Accessories"
        }
        response = requests.post(f"{BASE_URL}/products", json=payload)
        if response.status_code == 201 and "Keyboard" in response.text:
            self.passed("POST /products passed.")
        else:
            self.failed(f"POST /products failed. Response: {response.text}")

    @aetest.test
    def test_update_product(self):
        """Test updating a product."""
        payload = {"price": 30, "quantity": 90}
        response = requests.put(f"{BASE_URL}/products/2", json=payload)
        if response.status_code == 200 and "30" in response.text and "90" in response.text:
            self.passed("PUT /products/2 passed.")
        else:
            self.failed(f"PUT /products/2 failed. Response: {response.text}")

    @aetest.test
    def test_delete_product(self):
        """Test deleting a product."""
        response = requests.delete(f"{BASE_URL}/products/1")
        if response.status_code == 200 and "Product deleted" in response.text:
            self.passed("DELETE /products/1 passed.")
        else:
            self.failed(f"DELETE /products/1 failed. Response: {response.text}")

class CommonCleanup(aetest.CommonCleanup):
    """Cleanup actions after tests."""

    @aetest.subsection
    def cleanup(self):
        """Perform cleanup if needed."""
        print("Tests completed. API still running.")

if __name__ == '__main__':
    aetest.main()
