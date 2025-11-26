# 🏗️ Mechanic Shop Database API

A fully modular RESTful API for managing  **customers** ,  **mechanics** ,  **service tickets** , and **inventory parts** in a mechanic shop. Built using Flask, SQLAlchemy, and Marshmallow with support for caching, rate-limiting, validation, and Swagger API documentation.

---

## 🔹 Project Overview

### `__init__.py`

* Implements the `create_app()` factory function.
* Registers all blueprints and URL prefixes.
* Initializes extensions:
  * Marshmallow
  * Flask-Limiter
  * Flask-Caching
  * SQLAlchemy
* Loads configuration for development, testing, and production.

### `models.py`

Defines the main database models:

* **Customers**
* **Mechanics**
* **Service_Tickets**
* **Inventory** – parts used in tickets
* **ServicePart** – many-to-many association between tickets and inventory

### `extensions/`

Initializes and configures:

* Marshmallow (`ma`)
* Flask-Limiter (`limiter`)
* Flask-Caching (`cache`)

### `utils/base/`

Utility functions for:

* Password encoding/decoding
* Token generation
* Safe data handling

---

## 📂 Blueprint Structure

Each module has its own folder containing:

* `__init__.py` – initializes the blueprint
* `schema.py` – Marshmallow schemas for validation
* `routes.py` – CRUD routes and business logic

Blueprints include:

* **Customers**
* **Mechanics**
* **Service Tickets**
* **Inventory**

---

## ⚙️ Features

### ✔ Customers

* CRUD operations
* Pagination
* Token-based auth for protected routes

### ✔ Mechanics

* CRUD operations
* Sort mechanics by number of service tickets

### ✔ Service Tickets

* Create, view, and update service tickets
* Assign/remove mechanics
* Add/remove inventory parts using the `ServicePart` relationship

### ✔ Inventory

* CRUD operations
* Track quantity used in tickets

### ✔ Utilities

* Secure encoding/decoding
* Query-based pagination
* API caching
* Rate limiting

---

## 🧪 Unit Testing

Unit tests are stored inside the `/tests` directory and use `unittest`.

### Running Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 💻 Technologies Used

* Python 3.11+
* Flask
* Flask-SQLAlchemy
* Flask-Marshmallow
* Marshmallow-SQLAlchemy
* Flask-Caching
* Flask-Limiter
* Flasgger (Swagger UI)
* MySQL (mysqlconnector)

---

If you'd like, I can expand this README with diagrams, examples, or deployment instructions.
