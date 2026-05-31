<<<<<<< HEAD
# 🌿 Organic Food Store — Flask + MongoDB Atlas

A full-stack organic food e-commerce web app built with Flask and MongoDB Atlas.

---

## 📁 Project Structure

```
organic_food_store/
├── app.py                  ← Main Flask application (all routes)
├── config.py               ← MongoDB URI & Secret Key config
├── seed_db.py              ← Auto-populates Atlas with sample products
├── requirements.txt        ← Python dependencies
├── .env                    ← Your environment variables (credentials)
│
├── models/
│   ├── user.py             ← create_user, validate_user
│   ├── product.py          ← get_all_products, add_product, delete_product
│   └── order.py            ← create_order, get_all_orders
│
├── utils/
│   └── db_connection.py    ← get_db() — singleton MongoDB connection
│
├── templates/
│   ├── base.html           ← Navbar, footer, flash messages (shared layout)
│   ├── index.html          ← Home page
│   ├── products.html       ← Product listing + search results
│   ├── product_detail.html ← Single product page (dynamic from DB)
│   ├── cart.html           ← Shopping cart
│   ├── checkout.html       ← Checkout form
│   ├── order_success.html  ← Order confirmation
│   ├── login.html          ← Login form
│   ├── register.html       ← Register form
│   ├── profile.html        ← User profile
│   ├── admin_dashboard.html← Admin: view products + orders
│   └── add_product.html    ← Admin: add new product
│
└── static/
    ├── css/style.css       ← Custom styles
    ├── js/script.js        ← Auto-dismiss alerts, image fallback
    └── images/             ← Static images (hero background)
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up your .env file
Edit `.env` and add your MongoDB Atlas URI:
```
SECRET_KEY=organic_secret_key_2024
MONGO_URI=mongodb+srv://USERNAME:PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 3. Run the app
```bash
python app.py
```

The app **automatically seeds 8 sample products** into Atlas on first run.

### 4. Open in browser
```
http://127.0.0.1:5000
```

---

## 🔗 All Available URLs

| URL | What it does |
|---|---|
| `/` | Home page |
| `/products` | View all products from MongoDB |
| `/product/<id>` | View single product detail |
| `/search?query=rice` | Search products |
| `/add_to_cart/<id>` | Add product to session cart |
| `/cart` | View cart |
| `/remove_from_cart/<id>` | Remove item from cart |
| `/clear_cart` | Clear entire cart |
| `/checkout` | Checkout page |
| `/confirm_order` | Place order (saves to MongoDB) |
| `/order_success` | Order success page |
| `/register` | Create account (saves to MongoDB) |
| `/login` | Login (checks MongoDB) |
| `/logout` | Logout |
| `/profile` | User profile |
| `/admin` | Admin dashboard |
| `/add_product` | Add new product to MongoDB |
| `/delete/<id>` | Delete product from MongoDB |

---

## 🐛 Bugs Fixed from Original

1. `models/order.py` — `from utils.db_connection.py import` → `.py` is invalid in Python imports
2. `login()` route — was checking `GET` instead of `POST` for form data
3. `add_to_cart()` — was reading `image` from `request.form` on a GET route (always crashes)
4. `cart()` — default was `[0]` (a list with number) instead of `[]`
5. `admin_routes.py` — hardcoded `"your_mongodb_connection_string"` placeholder
6. `utils/db_connection.py` — file was missing entirely (models couldn't import it)
7. `register()` — was storing users in memory list (`users = []`), lost on restart
8. `order_success.html` — `<a href="products.html">` was a file path, not a Flask URL
=======
# orgonic_food_store
>>>>>>> dd3934aeab841fb8a4e1923733df2e7a77a9af47
