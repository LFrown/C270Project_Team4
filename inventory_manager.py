from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# In-memory product list (acts as a simple database)
products = [
    {"id": 1, "name": "Laptop", "price": 1200, "quantity": 10, "category": "Electronics"},
    {"id": 2, "name": "Mouse", "price": 25, "quantity": 100, "category": "Accessories"}
]

# Helper function to find a product by ID
def find_product(product_id):
    return next((product for product in products if product["id"] == product_id), None)

# Route to display all products (UI)
@app.route('/')
def index():
    return render_template('index.html', products=products)

# Route to add a new product (UI)
@app.route('/add_product', methods=['POST'])
def add_product_ui():
    global products  # Ensure we're modifying the global products list
    new_product = {
        "id": len(products) + 1,
        "name": request.form["name"],
        "price": float(request.form["price"]),
        "quantity": int(request.form["quantity"]),
        "category": request.form["category"]
    }
    products.append(new_product)
    return redirect(url_for('index'))

# Route to delete a product by ID (UI)
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product_ui(product_id):
    global products  # Ensure we're modifying the global products list
    product = find_product(product_id)
    if product:
        products.remove(product)
    return redirect(url_for('index'))

# Route to get all products (API)
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": products}), 200

# Route to add a new product (API)
@app.route('/products', methods=['POST'])
def add_product():
    global products  # Ensure we're modifying the global products list
    new_product = request.json
    new_product["id"] = len(products) + 1
    products.append(new_product)
    return jsonify(new_product), 201

# Route to update a product by ID (API)
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = find_product(product_id)
    if product:
        updated_data = request.json
        product.update(updated_data)
        return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404

# Route to delete a product by ID (API)
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products  # Ensure we're modifying the global products list
    product = find_product(product_id)
    if product:
        products.remove(product)
        return jsonify({"message": "Product deleted"}), 200
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
