
# Employee Management System

A Python-based Employee Management System built with FastAPI and PostgreSQL. It provides REST API endpoints to manage employee records, including creating, viewing, updating, and deleting employees.

## Features

- Register new employees
- Retrieve all employee records
- Retrieve an employee by ID
- Update employee information
- Delete employee records
- Validate employee details using Pydantic
- Prevent duplicate employee IDs and email addresses
- Handle missing employee records with appropriate HTTP errors
- Store employee information in PostgreSQL
- Automated API tests using pytest

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- Psycopg
- Pydantic
- Pytest
- Uvicorn

## Project Structure

```text
employee_management/
├── app/
│   ├── .env
│   ├── api.py
│   ├── db_connection.py
│   ├── main.py
│   └── __init__.py
├── tests/
│   └── test_api.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd employee_management
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure database settings

Create an `.env` file inside the `app` folder with these settings:

```env
DB_HOST=localhost
DB_NAME=employee_management_db
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_PORT=5432
```

Replace the username and password with your own PostgreSQL credentials.

Create the `employees` table in your PostgreSQL database using the table definition in your project setup.

### 6. Run the application

From the project root:

```bash
python -m uvicorn app.api:app --reload
```

### 7. Access the API documentation

Open:

http://127.0.0.1:8000/docs

You can test the API endpoints through the interactive Swagger interface.

## Running Automated Tests

Run the following command from the project root:

```bash
python -m pytest -v
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check API status |
| GET | `/employees` | Retrieve all employees |
| GET | `/employees/{employee_id}` | Retrieve an employee |
| POST | `/employees` | Register an employee |
| PUT | `/employees/{employee_id}` | Update an employee |
| DELETE | `/employees/{employee_id}` | Delete an employee |

## Future Improvements

- Add structured application logging
- Improve database connection management
- Add authentication and authorization
- Deploy the API to a cloud platform
