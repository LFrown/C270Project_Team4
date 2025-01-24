from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

# In-memory product and category lists
products = [
    {"id": 1, "name": "Laptop", "price": 1200, "quantity": 10, "category": "Electronics"},
    {"id": 2, "name": "Mouse", "price": 25, "quantity": 100, "category": "Accessories"}
]

categories = [
    {"id": 1, "name": "Electronics"},
    {"id": 2, "name": "Accessories"}
]

# Helper function to find a product by ID
def find_product(product_id):
    return next((product for product in products if product["id"] == product_id), None)

# Helper function to find a category by ID
def find_category(category_id):
    return next((category for category in categories if category["id"] == category_id), None)

# Route to display all products and categories (UI)
@app.route('/')
def index():
    return render_template('index.html', products=products, categories=categories)

# Route to add a new product (UI)
@app.route('/add_product', methods=['POST'])
def add_product_ui():
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
    product = find_product(product_id)
    if product:
        products.remove(product)
    return redirect(url_for('index'))

# Route to add a new category (UI)
@app.route('/add_category', methods=['POST'])
def add_category_ui():
    new_category = {
        "id": len(categories) + 1,
        "name": request.form["name"]
    }
    categories.append(new_category)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
