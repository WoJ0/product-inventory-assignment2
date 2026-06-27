# Product Inventory Management System

**Assignment 2** — An application built with the **Flask** framework (Python) that
implements **five functionalities**, **two** of which are also exposed as
**RESTful web-services**.

---

## 1. Application

A simple Product Inventory system. Each product has an `id`, `name`,
`category`, `price`, and `quantity`. Data is stored in a SQLite database via
SQLAlchemy.

## 2. The Five (5) Functionalities

| # | Functionality | Web Page (HTML) | Description |
|---|---------------|-----------------|-------------|
| 1 | **Add** product    | `GET/POST /add`              | Create a new product |
| 2 | **List/View** products | `GET /`                  | Show all products in a table |
| 3 | **Update** product | `GET/POST /edit/<id>`        | Edit an existing product |
| 4 | **Delete** product | `POST /delete/<id>`          | Remove a product |
| 5 | **Search** products| `GET /?q=<term>`             | Filter by name or category |

## 3. The Two (2) RESTful Web-Services

Two of the functionalities above are **also** exposed as REST web-services that
return **JSON** (so they can be consumed by other apps, Postman, curl, etc.).

### REST Web Service 1 — Product resource (CRUD)

| Method | Endpoint                  | Purpose            | Maps to functionality |
|--------|---------------------------|--------------------|-----------------------|
| GET    | `/api/products`           | List all products  | #2 List/View |
| GET    | `/api/products/<id>`      | Get one product    | #2 List/View |
| POST   | `/api/products`           | Create a product   | #1 Add |
| PUT    | `/api/products/<id>`      | Update a product   | #3 Update |
| DELETE | `/api/products/<id>`      | Delete a product   | #4 Delete |

### REST Web Service 2 — Product search

| Method | Endpoint                          | Purpose                       | Maps to functionality |
|--------|-----------------------------------|-------------------------------|-----------------------|
| GET    | `/api/products/search?q=<term>`   | Search products, return JSON  | #5 Search |

---

## 4. How to Set Up the Framework & Run

> Requires **Python 3.8+**

```bash
# 1. (optional) create a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 2. install the Flask framework and dependencies
pip install -r requirements.txt

# 3. run the application
python app.py
```

Then open your browser at: **http://127.0.0.1:5000**

The database (`inventory.db`) and 3 sample products are created automatically
on first run.

---

## 5. Testing the REST Web-Services

Using **curl** (or import into Postman):

```bash
# List all products
curl http://127.0.0.1:5000/api/products

# Get one product
curl http://127.0.0.1:5000/api/products/1

# Create a product
curl -X POST http://127.0.0.1:5000/api/products \
     -H "Content-Type: application/json" \
     -d '{"name":"USB Cable","category":"Electronics","price":5.99,"quantity":120}'

# Update a product
curl -X PUT http://127.0.0.1:5000/api/products/1 \
     -H "Content-Type: application/json" \
     -d '{"price":17.50,"quantity":40}'

# Delete a product
curl -X DELETE http://127.0.0.1:5000/api/products/1

# Search (REST)
curl "http://127.0.0.1:5000/api/products/search?q=electronics"
```

---

## 6. Project Structure

```
product-inventory/
├── app.py              # Flask app: web routes + REST API
├── models.py           # SQLAlchemy Product model
├── requirements.txt    # Framework dependencies
├── templates/          # HTML pages (Jinja2)
│   ├── base.html
│   ├── index.html      # list + search
│   └── form.html       # add + edit
├── static/
│   └── style.css
├── .gitignore
└── README.md
```

---

## 7. Tech Stack
- **Framework:** Flask 3 (Python)
- **ORM / Database:** Flask-SQLAlchemy + SQLite
- **Templating:** Jinja2
- **REST format:** JSON
