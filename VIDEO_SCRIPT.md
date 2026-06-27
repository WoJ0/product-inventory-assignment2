# Video Script (target: under 2 minutes)

Record your screen (OBS, Zoom, or Windows Game Bar `Win+G`). Export as `.mp4`,
under 200 MB. Keep it tight — read the lines below while you click.

---

## [0:00–0:15] Intro
> "Hi, this is my Assignment 2. I built a **Product Inventory** application using
> the **Flask framework** in Python. It has five functionalities, and two of them
> are exposed as RESTful web-services. Here is my GitHub repository."

*(Show the GitHub page briefly.)*   

---

## [0:15–0:40] How I set up the framework
*(Show the project files in your editor.)*
> "Flask is installed from `requirements.txt` using `pip install -r requirements.txt`.
> In `app.py` I create the Flask app, configure a SQLite database with
> SQLAlchemy, and define my routes. I run it with `python app.py`."

*(Run `python app.py` in the terminal, show it start on port 5000.)*

---

## [0:40–1:10] Demo of the 5 functionalities
*(Open http://127.0.0.1:5000)*
> "Functionality 1 and 2 — I can **add** a product and **view** the list here.
> Functionality 3 — I'll **edit** this product's price.
> Functionality 4 — I'll **delete** a product.
> Functionality 5 — I'll **search** by category."

*(Click through: Add → Edit → Delete → type in the search box.)*

---

## [1:10–1:45] How I set up the RESTful web-services
*(Open Postman or a terminal with curl.)*
> "Two functionalities are also RESTful web-services that return JSON.
> The first is the **Product CRUD API** at `/api/products` — here's a GET
> returning all products as JSON, and a POST that creates one.
> The second is the **search API** at `/api/products/search?q=` — it returns
> matching products as JSON."

*(Show: GET /api/products, POST /api/products, GET /api/products/search?q=electronics)*

---

## [1:45–2:00] Close
> "So that's five functionalities with two RESTful web-services, built on Flask.
> The full source code is in the GitHub link in the description. Thank you."

---

### Quick demo commands (paste into terminal during recording)
```bash
curl http://127.0.0.1:5000/api/products
curl -X POST http://127.0.0.1:5000/api/products -H "Content-Type: application/json" -d "{\"name\":\"USB Cable\",\"category\":\"Electronics\",\"price\":5.99,\"quantity\":120}"
curl "http://127.0.0.1:5000/api/products/search?q=electronics"
```
