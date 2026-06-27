"""
Product Inventory Management System
Assignment 2 - Flask Framework with RESTful Web Services

Five functionalities:
  1. Add a product
  2. List / view products
  3. Update a product
  4. Delete a product
  5. Search products

Two of the five are also exposed as RESTful web-services (returning JSON):
  - REST Web Service 1: Product resource CRUD  -> /api/products ...
  - REST Web Service 2: Product search         -> /api/products/search
"""

from flask import (
    Flask, render_template, request, redirect, url_for, flash, jsonify
)
from models import db, Product

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "assignment2-secret-key"

db.init_app(app)


def seed_if_empty():
    """Add a few sample products on first run so the app isn't empty."""
    if Product.query.count() == 0:
        samples = [
            Product(name="Wireless Mouse", category="Electronics", price=19.99, quantity=50),
            Product(name="Notebook A5", category="Stationery", price=3.50, quantity=200),
            Product(name="Coffee Mug", category="Kitchen", price=8.25, quantity=75),
        ]
        db.session.add_all(samples)
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_if_empty()


# ---------------------------------------------------------------------------
# WEB INTERFACE (HTML)  -  Functionalities 1 to 5
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Functionality 2: List / view all products (and Functionality 5: search)."""
    query = request.args.get("q", "").strip()
    if query:
        like = f"%{query}%"
        products = Product.query.filter(
            db.or_(Product.name.ilike(like), Product.category.ilike(like))
        ).all()
    else:
        products = Product.query.order_by(Product.id).all()
    return render_template("index.html", products=products, query=query)


@app.route("/add", methods=["GET", "POST"])
def add_product():
    """Functionality 1: Add a product."""
    if request.method == "POST":
        try:
            product = Product(
                name=request.form["name"].strip(),
                category=request.form["category"].strip(),
                price=float(request.form["price"]),
                quantity=int(request.form["quantity"]),
            )
        except (ValueError, KeyError):
            flash("Invalid input. Please check the values.", "error")
            return redirect(url_for("add_product"))

        db.session.add(product)
        db.session.commit()
        flash(f'Product "{product.name}" added successfully.', "success")
        return redirect(url_for("index"))
    return render_template("form.html", product=None, action="Add")


@app.route("/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    """Functionality 3: Update a product."""
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        try:
            product.name = request.form["name"].strip()
            product.category = request.form["category"].strip()
            product.price = float(request.form["price"])
            product.quantity = int(request.form["quantity"])
        except (ValueError, KeyError):
            flash("Invalid input. Please check the values.", "error")
            return redirect(url_for("edit_product", product_id=product_id))

        db.session.commit()
        flash(f'Product "{product.name}" updated successfully.', "success")
        return redirect(url_for("index"))
    return render_template("form.html", product=product, action="Edit")


@app.route("/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    """Functionality 4: Delete a product."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash(f'Product "{product.name}" deleted.', "success")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------------
# REST WEB SERVICE 1:  Product resource CRUD  (returns JSON)
# ---------------------------------------------------------------------------

@app.route("/api/products", methods=["GET"])
def api_list_products():
    """GET all products as JSON."""
    products = Product.query.order_by(Product.id).all()
    return jsonify([p.to_dict() for p in products]), 200


@app.route("/api/products/<int:product_id>", methods=["GET"])
def api_get_product(product_id):
    """GET a single product as JSON."""
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict()), 200


@app.route("/api/products", methods=["POST"])
def api_create_product():
    """POST a new product (JSON body) -> creates and returns it."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required = ["name", "category", "price", "quantity"]
    missing = [field for field in required if field not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        product = Product(
            name=str(data["name"]).strip(),
            category=str(data["category"]).strip(),
            price=float(data["price"]),
            quantity=int(data["quantity"]),
        )
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data types"}), 400

    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201


@app.route("/api/products/<int:product_id>", methods=["PUT"])
def api_update_product(product_id):
    """PUT updates an existing product (JSON body)."""
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    try:
        if "name" in data:
            product.name = str(data["name"]).strip()
        if "category" in data:
            product.category = str(data["category"]).strip()
        if "price" in data:
            product.price = float(data["price"])
        if "quantity" in data:
            product.quantity = int(data["quantity"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data types"}), 400

    db.session.commit()
    return jsonify(product.to_dict()), 200


@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def api_delete_product(product_id):
    """DELETE a product."""
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted", "id": product_id}), 200


# ---------------------------------------------------------------------------
# REST WEB SERVICE 2:  Product search  (returns JSON)
# ---------------------------------------------------------------------------

@app.route("/api/products/search", methods=["GET"])
def api_search_products():
    """GET /api/products/search?q=<term> -> matching products as JSON."""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    like = f"%{query}%"
    products = Product.query.filter(
        db.or_(Product.name.ilike(like), Product.category.ilike(like))
    ).all()
    return jsonify({
        "query": query,
        "count": len(products),
        "results": [p.to_dict() for p in products],
    }), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
