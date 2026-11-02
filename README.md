# Django eCommerce Application

## Project Description

The Django eCommerce Application is a web-based shopping platform developed for the HyperionDev Django eCommerce assignment.

Users can register as buyers or vendors. Vendors can manage their stores and products, while buyers can browse products, add items to a shopping cart, place orders, and submit product reviews.

## Features

### User Accounts
- User registration with email collection and duplicate email validation.
- Separate buyer and vendor account types.
- Role-based dashboards.
- Login and logout functionality.
- Password reset using unique, temporary tokens with expiration times.

### Vendor and Store Management
- Create, edit, and delete stores.
- Create, edit, and delete products.
- Manage product descriptions, prices, and stock quantities.
- Restrict store and product management to the appropriate vendor.

### Shopping and Orders
- Browse products from different stores.
- Select product quantities when adding items to the shopping cart.
- Validate available stock before adding products to the cart.
- View cart quantities, subtotals, and totals.
- Remove individual products or clear the entire cart.
- Complete checkout and create orders.
- Update product stock after checkout.
- Generate order invoices containing purchased products, quantities, prices, and totals.
- Send invoice email content through Django's configured email backend.

### Product Reviews
- Submit product comments and ratings.
- Rate products from 1 to 5.
- Identify reviews from verified purchasers.
- Allow buyers to submit multiple reviews for the same product over time.

### User Interface
- HTML templates styled with Bootstrap.
- Separate pages for account management, dashboards, products, stores, shopping carts, checkout, and reviews.
- Logout options on buyer shopping pages.

## Technologies Used

- Python
- Django
- HTML and CSS
- Bootstrap
- Django ORM
- MySQL

## Project Structure

```text
Django_eCommerce_Final/
├── accounts/
├── products/
├── stores/
├── orders/
├── ecommerce_project/
├── Practical_Task_2_Research_Answers.docx
├── Project_Planning_Documentation.docx
├── manage.py
├── requirements.txt
└── README.md
```

The application also includes templates, migrations, and tests within the relevant application folders.

## Installation and Setup

### 1. Clone the GitHub Repository

Replace `<repo-link>` with the actual URL of the GitHub repository.

```bash
git clone https://github.com/Siyamcela2014/Django_eCommerce_Final.git
```

### 2. Enter the Project Directory

```bash
cd Django_eCommerce_Final
```

### 3. Create a Virtual Environment

Create the virtual environment inside the project directory.

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Configuration

The application uses MySQL.

### 1. Log in to MySQL

Open a terminal and run:

```bash
mysql -u root -p
```

Enter your MySQL root password when prompted.

### 2. Create the Database

Run the following SQL query:

```sql
CREATE DATABASE ecommerce_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 3. Exit MySQL

```sql
exit;
```

### 4. Configure Django

Check the database configuration in:

```text
ecommerce_project/settings.py
```

Ensure the database name, username, password, host, and port match your local MySQL configuration.

Keep database passwords and secret keys out of public source control. Use environment variables for sensitive configuration.

## Apply Database Migrations

Run:

```bash
python manage.py migrate
```

## Start the Development Server

Run:

```bash
python manage.py runserver
```

## Open the Application

Visit:

http://127.0.0.1:8000/

The project's root URL is configured to redirect to the product browsing page.

## Testing

Run the Django system check:

```bash
python manage.py check
```

Run the automated test suite:

```bash
python manage.py test
```

The automated tests cover account and product functionality.

## Email Configuration

The project uses Django's configured email backend. When the console email backend is enabled, generated email content is displayed in the terminal instead of being delivered to a real email inbox.

For actual email delivery, configure an appropriate email backend and its credentials.

## Security Notes

- Do not commit passwords, secret keys, or other sensitive credentials to a public repository.
- Use Django's password-handling functions to securely set passwords.
- Password-reset tokens should be unique, expire, and be marked as used after a successful reset.
- The Django development server is intended for development and testing, not production deployment.

## Assignment

Developed as part of the HyperionDev Django eCommerce Application assignment.
## Windows Setup

1. Install Python 3.13 and MySQL Server.
2. Create a virtual environment: `python -m venv venv`.
3. Activate it: `.\venv\Scripts\Activate.ps1`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Copy configuration: `Copy-Item .env.example .env`.
6. Add your own SECRET_KEY and MySQL DB_PASSWORD to .env.
7. Create the MySQL database named ecommerce_db.
8. Run migrations: `python manage.py migrate`.
9. Start the application: `python manage.py runserver`.
10. Run tests: `python manage.py test`.

Never commit .env or expose passwords and secret keys.
