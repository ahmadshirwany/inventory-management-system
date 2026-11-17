# Inventory Management System

A web-based agricultural & warehouse inventory management dashboard built with **Django 5.1.6**, **Bootstrap / Material Dashboard UI**, and **SQLite** (ready for PostgreSQL/MySQL).

It supports multi-tenant warehouse operations with role-based access control for **Superusers (Admins)**, **Owners**, **Employees**, **Farmers**, and **Clients (Customers)**, complete with batch/lot tracking, storage condition metadata, and customer item request fulfillment.

---

## ✨ Key Features

- **Role-Based Multi-User Access**
  - **Superuser (Admin)**: Full system control, manage owners, warehouses, product metadata (`products.json`), and Django Admin.
  - **Owner**: Create and manage warehouses (within subscription plan limits), manage employees, farmers, and clients, assign users to warehouses, and approve/complete customer requests.
  - **Employee (`user`)**: View assigned warehouses, manage stock (add/take out products), view farmers & clients, and process item requests for assigned warehouses.
  - **Farmer**: View assigned warehouses and supply/add products.
  - **Client (Customer)**: Browse aggregated in-stock products in assigned warehouses, submit weight-based item requests with automatic price calculation, and track request status.
- **Warehouse Management**
  - Create and edit warehouses (`General`, `Cold Storage`, `Bonded`, `Automated`) with automatic URL slug generation, capacity/available space validation, and automatic utilization rate calculation.
  - Assign employees, clients, and farmers per warehouse.
  - Subscription plan warehouse limits (`Basic`: 3, `Pro`: 5, `Premium`: 10).
- **Product & Inventory Tracking**
  - Auto-generated unique **SKU** (`WH-<warehouse_id>-<seq>`), **12-digit Barcode** (for Raw products), and **Lot Number** (`LOT-YYYYMMDD-XXXXXX`).
  - Automatic population of storage conditions (temperature, humidity, CO₂, O₂, N₂, ethylene management, expiration date, notes) from `apps/managment/products.json`.
  - Support for both **Bulk** and **Packaged** goods (`weight_per_bag_kg`, `quantity_in_stock`, total weight in kg/g, and total value calculation).
  - **Take Out Stock** workflow that proportionally adjusts both unit quantity and weight and automatically marks depleted stock as `Out of Stock` with an exit date.
  - Filtering, sorting, and pagination across all inventory lists.
- **Customer Item Requests & FIFO Fulfillment**
  - Clients can request available products by weight from their assigned warehouses.
  - Owners/employees can **Approve**, **Reject**, or **Complete** requests.
  - Completing a request automatically deducts stock from matching warehouse batches ordered by **nearest expiration date**, then entry date.
- **Product Metadata Manager (Superuser)**
  - Dedicated UI (`/manage-product-metadata/`) to add, edit, and delete product storage metadata entries stored in `apps/managment/products.json` with live cache refresh.
- **User Accounts & Profiles**
  - Login via **username or email** (`EmailOrUsernameBackend`).
  - Password strength validation (8+ chars, uppercase, lowercase, number, special character).
  - Profile page for password updates and profile picture uploads.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, Django 5.1.6
- **Frontend**: Django Templates, Material Dashboard UI, Bootstrap 5, Select2, jQuery
- **Database**: SQLite3 (default; configurable for PostgreSQL/MySQL)
- **Static & Media**: WhiteNoise, Pillow
- **Deployment**: Docker, Docker Compose, Gunicorn, Nginx

---

## 📂 Project Structure

```text
Inventory_System/
├── apps/
│   ├── authentication/          # CustomUser, Farmer, Client models, auth views, forms, signals, backends
│   ├── managment/               # Warehouse, Product, ProductLog, ItemRequest models, views, forms, admin
│   │   └── products.json        # (Gitignored) Product storage metadata catalog
│   ├── static/                  # CSS, JavaScript, images, favicon
│   └── templates/
│       ├── accounts/            # Login, register, create user, user/farmer/client lists & modals
│       ├── home/                # Error pages (page-403.html, page-404.html, page-500.html)
│       ├── includes/            # Sidebar, navigation, footer, pagination, scripts
│       ├── layouts/             # Base HTML layout (base.html)
│       └── managment/           # Dashboard, warehouses, products, requests, metadata, profile
├── core/
│   ├── settings.py              # Django settings (env-driven DEBUG, SECRET_KEY, ALLOWED_HOSTS, CSRF)
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py / asgi.py        # WSGI / ASGI entry points
│   └── media/                   # (Gitignored) Uploaded profile pictures
├── nginx/
│   └── inventory-app.conf       # Nginx reverse proxy configuration (port 85 -> Gunicorn 5005)
├── Dockerfile                   # Python 3.11 + Gunicorn container
├── docker-compose.yml           # App + Nginx services
├── gunicorn-cfg.py              # Gunicorn server config
├── manage.py                    # Django management script
└── requirements.txt             # Python dependencies
```

---

## 🔐 Environment & Configuration

Create a `.env` file in the project root (not tracked by Git):

```env
DEBUG=True
SECRET_KEY=replace-with-a-strong-random-secret-key
SERVER=localhost
```

Optionally create `IP_data.json` in the project root if you need an extra host IP added to `ALLOWED_HOSTS` (defaults safely to `127.0.0.1` if omitted):

```json
{
  "IP": "127.0.0.1"
}
```

> **Note**: `apps/managment/products.json` is gitignored. Ensure it exists (or add products via `/manage-product-metadata/` as a superuser) so product choices are available when adding inventory.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python **3.10+** (Python **3.11** recommended)
- `pip`

### 1. Clone & Create a Virtual Environment

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\activate.ps1
```

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Apply Database Migrations

```bash
python manage.py migrate
```

### 4. Create a Superuser Account

```bash
python manage.py createsuperuser
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Or on a custom port (e.g., if port `8000` is already in use):

```bash
python manage.py runserver 8080
```

Open **http://127.0.0.1:8000/** in your browser and sign in.

---

## 🐳 Running with Docker

1. Make sure Docker and Docker Compose are installed and `.env` is configured.
2. Build and start the containers:
   ```bash
   docker-compose up -d --build
   ```
3. Access the application via Nginx at:
   ```text
   http://localhost:85
   ```
4. Stop the containers:
   ```bash
   docker-compose down
   ```

---

## 🗺️ Main Application Routes

| Route | Description | Allowed Roles |
| --- | --- | --- |
| `/` | Main dashboard (warehouses, employee & customer stats) | All authenticated |
| `/login/`, `/register/`, `/logout/` | Authentication endpoints | Public / Authenticated |
| `/user-profile/` | View profile, change password, upload profile picture | All authenticated |
| `/warehouses-list/` | View/filter warehouses & edit modal | All authenticated (edit: Owner/Superuser) |
| `/create-warehouse/` | Create a new warehouse | Owner, Superuser |
| `/warehouses-list/<slug>/` | Manage warehouse products (add, take out, delete) | Assigned users, Owner, Superuser |
| `/warehouses-list/<slug>/customer` | Browse aggregated warehouse stock & submit requests | Client |
| `/user-list/`, `/create-user/` | View, create, edit, and delete employees/users | Owner, Superuser |
| `/farmers/` | View, create, edit, and delete farmers | Superuser, Owner, Employee (view only) |
| `/clients/` | View, create, edit, and delete clients | Superuser, Owner, Employee (view only) |
| `/requests/` | Approve, reject, and complete client item requests | Superuser, Owner, Employee |
| `/customer/requests/` | Track submitted item requests | Client |
| `/manage-product-metadata/` | Add, edit, and delete product metadata catalog | Superuser |
| `/admin/` | Django Admin interface | Staff / Superuser |

---

## 🐛 Troubleshooting

- **Browser hangs or shows another app on port `8000`**: Another local server is likely holding port `8000`. Run on another port: `python manage.py runserver 8080`.
- **CSRF verification failed (403)**: Ensure your host/origin is listed in `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` in [core/settings.py](core/settings.py).
- **Empty product dropdown when adding a product**: Add product entries at `/manage-product-metadata/` (as a superuser) or place a valid `products.json` file in `apps/managment/products.json`.
- **Verify Django setup**:
  ```bash
  python manage.py check
  ```

---

## 📄 License

MIT License — see [LICENSE.md](LICENSE.md) for details.
