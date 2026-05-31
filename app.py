from flask import Flask, render_template, request, redirect, url_for, flash, session
from bson.objectid import ObjectId
from config import Config
from utils.db_connection import get_db
from models.user import create_user, validate_user
from models.product import get_all_products, get_product_by_id, add_product, delete_product, search_products
from models.order import create_order
from seed_db import seed

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

# Auto-seed database on first run
with app.app_context():
    try:
        seed()
    except Exception as e:
        print(f"Seed skipped: {e}")

# ─────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

# ─────────────────────────────────────────────
#  PRODUCTS
# ─────────────────────────────────────────────
@app.route("/products")
def products():
    product_list = get_all_products()
    return render_template("products.html", products=product_list)

@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    product_list = search_products(query) if query else []
    return render_template("products.html", products=product_list, search_query=query)

# ─────────────────────────────────────────────
#  PRODUCT DETAIL PAGE  (dynamic — from DB)
# ─────────────────────────────────────────────
@app.route("/product/<product_id>")
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash("Product not found!", "danger")
        return redirect(url_for("products"))
    return render_template("product_detail.html", product=product)

# ─────────────────────────────────────────────
#  INDIVIDUAL STATIC PRODUCT PAGES (kept for backward compat)
# ─────────────────────────────────────────────
@app.route("/beetrot")
def beetrot():
    product = {"name": "Beetroot", "price": 70,
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Rote_Beete.jpg/640px-Rote_Beete.jpg",
                "description": "Fresh organic beetroot rich in iron and vitamins."}
    return render_template("product_info.html", product=product)

@app.route("/caroot")
def caroot():
    product = {"name": "Carrot", "price": 60,
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Vegetable-Carrot-Bundle-wStalks.jpg/640px-Vegetable-Carrot-Bundle-wStalks.jpg",
                "description": "Crunchy organic carrots loaded with beta-carotene."}
    return render_template("product_info.html", product=product)

@app.route("/muttaikosh")
def muttaikosh():
    product = {"name": "Muttaikosh", "price": 88,
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Cauliflower_2.jpg/640px-Cauliflower_2.jpg",
                "description": "Fresh organic cauliflower, great for health."}
    return render_template("product_info.html", product=product)

@app.route("/kavuni")
def kavuni():
    product = {"name": "Kavuni Rice", "price": 223,
                "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Ricefield.jpg/640px-Ricefield.jpg",
                "description": "Traditional black kavuni rice with high antioxidants."}
    return render_template("product_info.html", product=product)

# ─────────────────────────────────────────────
#  CART
# ─────────────────────────────────────────────
@app.route("/add_to_cart/<product_id>")
def add_to_cart(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash("Product not found!", "danger")
        return redirect(url_for("products"))

    if "cart" not in session:
        session["cart"] = []

    # Check if already in cart
    for item in session["cart"]:
        if item["id"] == product_id:
            item["qty"] = item.get("qty", 1) + 1
            session.modified = True
            flash(f"{product['name']} quantity updated in cart!", "success")
            return redirect(url_for("products"))

    session["cart"].append({
        "id": product_id,
        "name": product["name"],
        "price": product["price"],
        "image": product.get("image", ""),
        "qty": 1
    })
    session.modified = True
    flash(f"{product['name']} added to cart!", "success")
    return redirect(url_for("products"))

@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = sum(item["price"] * item.get("qty", 1) for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)

@app.route("/remove_from_cart/<product_id>")
def remove_from_cart(product_id):
    if "cart" in session:
        session["cart"] = [i for i in session["cart"] if i["id"] != product_id]
        session.modified = True
    flash("Item removed from cart.", "info")
    return redirect(url_for("cart"))

@app.route("/clear_cart")
def clear_cart():
    session.pop("cart", None)
    flash("Cart cleared.", "info")
    return redirect(url_for("cart"))

# ─────────────────────────────────────────────
#  CHECKOUT & ORDER
# ─────────────────────────────────────────────
@app.route("/checkout")
def checkout():
    cart_items = session.get("cart", [])
    if not cart_items:
        flash("Your cart is empty!", "warning")
        return redirect(url_for("products"))
    total = sum(item["price"] * item.get("qty", 1) for item in cart_items)
    return render_template("checkout.html", cart=cart_items, total=total)

@app.route("/confirm_order", methods=["POST"])
def confirm_order():
    cart_items = session.get("cart", [])
    customer_name = request.form.get("name", "")
    phone = request.form.get("phone", "")
    address = request.form.get("address", "")

    if not cart_items:
        flash("No items to order!", "danger")
        return redirect(url_for("products"))

    for item in cart_items:
        create_order(
            product_name=item["name"],
            price=item["price"] * item.get("qty", 1),
            customer_name=customer_name,
            phone=phone,
            address=address,
            cod=True
        )

    session.pop("cart", None)
    flash("Order placed successfully!", "success")
    return redirect(url_for("order_success"))

@app.route("/order_success")
def order_success():
    return render_template("order_success.html")

# ─────────────────────────────────────────────
#  AUTH — REGISTER & LOGIN
# ─────────────────────────────────────────────
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            flash("All fields are required!", "danger")
            return render_template("register.html")

        db = get_db()
        if db.users.find_one({"email": email}):
            flash("Email already registered. Please login.", "warning")
            return redirect(url_for("login"))

        create_user(name, email, password)
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":                       # FIX: was checking GET
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        user = validate_user(email, password)

        if user:
            session["user"]  = user["name"]
            session["email"] = user["email"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("home"))

        flash("Invalid email or password!", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))

# ─────────────────────────────────────────────
#  ADMIN ROUTES
# ─────────────────────────────────────────────
@app.route("/admin")
def admin_dashboard():
    products = get_all_products()
    orders   = []
    try:
        from models.order import get_all_orders
        orders = get_all_orders()
    except Exception:
        pass
    return render_template("admin_dashboard.html", products=products, orders=orders)

@app.route("/add_product", methods=["GET", "POST"])
def add_product_route():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        category = request.form.get("category", "").strip()
        price    = request.form.get("price", 0)
        quantity = request.form.get("quantity", 0)
        image    = request.form.get("image", "").strip()

        add_product(name, category, price, quantity, image)
        flash(f"Product '{name}' added successfully!", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("add_product.html")

@app.route("/delete/<product_id>")
def delete_product_route(product_id):
    delete_product(product_id)
    flash("Product deleted!", "danger")
    return redirect(url_for("admin_dashboard"))

# ─────────────────────────────────────────────
#  PROFILE
# ─────────────────────────────────────────────
@app.route("/profile")
def profile():
    if "user" not in session:
        flash("Please login to view your profile.", "warning")
        return redirect(url_for("login"))
    return render_template("profile.html", user=session["user"], email=session.get("email", ""))

# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
