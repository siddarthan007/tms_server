# Theatre Management System API

The Theatre Management System API is a backend service built with FastAPI to manage theatre operations, including customer registration, admin management, bookings, and more. It uses SQLite as its database and provides a RESTful interface for theatre-related functionalities.

## Features
- Customer registration and management
- Admin authentication and role-based access
- Theatre, screen, seat, and show management
- Booking and ticketing system
- Audit logging for admin actions

## Tech Stack
- **Framework**: FastAPI
- **Database**: SQLite
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt via `passlib`
- **Python Version**: 3.12
- **Dependencies**: Managed via `requirements.txt`

## Prerequisites
- Python 3.12+
- Miniforge3 or another Python environment manager (e.g., virtualenv)
- Git (optional, for version control)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd theatre_management_system
```

### 2. Set Up the Environment
Using Miniforge3:
```bash
conda create -n tms python=3.12
conda activate tms
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize the Database
The SQLite database (`theatre.db`) is created automatically on first run:
```bash
python app.py
```
- Schema is defined in `database/schema.sql` and initialized via `database/init_db.py`.

### 5. Run the Server
```bash
python app.py
```
- The API will be available at `http://localhost:8000`.
- Access the interactive API docs at `http://localhost:8000/docs`.

## Usage

### Authentication
- **Admin Login**: Obtain a JWT token for admin actions.
  ```bash
  curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
  ```
- Use the `access_token` in the `Authorization` header: `Bearer <token>`.

### Example Endpoints
- **Register a Customer** (Public):
  ```bash
  curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Customer", "email": "customer@example.com", "phone_number": "9876543210", "username": "newcustomer", "password": "cust123"}'
  ```
  - Response: `{"message": "Customer registered", "customer_id": 1}`

- **Get All Customers** (Admin-only):
  ```bash
  curl -X GET "http://localhost:8000/customers/" \
  -H "Authorization: Bearer <token>"
  ```

See `http://localhost:8000/docs` for the full API specification.

## Project Structure
```
theatre_management_system/
├── app.py               # Main application entry point
├── requirements.txt     # Dependencies
├── .gitignore          # Git ignore file
├── database/
│   ├── connection.py   # Database connection logic
│   ├── init_db.py      # Database initialization
│   ├── schema.sql      # SQLite schema
│   └── theatre.db      # SQLite database (ignored by Git)
├── models/             # Pydantic models
├── repositories/       # Data access layer
├── routes/             # API endpoints
├── services/           # Business logic
└── utils/              # Utilities (JWT, hashing)
```

## License
This project is licensed under the MIT License.

## Contact
For issues or suggestions, please open an issue on the repository or contact the maintainer at `<siddarthanepal5@gmail.com>`.