from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


def test_home():
    
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Employee Management API is running"
    }
def test_get_all_employees():
    response = client.get("/employees")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_get_employee_by_id():
    response = client.get("/employees/EMP203")

    assert response.status_code == 200
    assert response.json()["employee_id"] == "EMP203"
def test_employee_not_found():
    response = client.get("/employees/EMP99999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Employee not found"
    }
def test_invalid_employee_id():
    employee_data = {
        "employee_id": "ABC123",
        "name": "Arjun",
        "email": "arjun@example.com",
        "department": "IT",
        "salary": 45000,
        "age": 25,
        "location": "Hyderabad"
    }

    response = client.post("/employees", json=employee_data)

    assert response.status_code == 422

def test_invalid_salary():
    employee_data = {
        "employee_id": "EMP90001",
        "name": "Neha",
        "email": "neha@example.com",
        "department": "HR",
        "salary": 0,
        "age": 28,
        "location": "Hyderabad"
    }

    response = client.post("/employees", json=employee_data)

    assert response.status_code == 422

def test_update_employee():
    updated_data = {
        "name": "Arjun Updated",
        "email": "arjun.updated@example.com",
        "department": "Data Engineering",
        "salary": 55000,
        "age": 26,
        "location": "Hyderabad"
    }

    response = client.put(
        "/employees/EMP203",
        json=updated_data
    )

    assert response.status_code == 200

def test_delete_employee():
    employee_data = {
        "employee_id": "EMP90002",
        "name": "Neha",
        "email": "neha.delete@example.com",
        "department": "HR",
        "salary": 40000,
        "age": 28,
        "location": "Hyderabad"
    }

    create_response = client.post(
        "/employees",
        json=employee_data
    )

    assert create_response.status_code == 200

    delete_response = client.delete("/employees/EMP90002")

    assert delete_response.status_code == 200

def test_delete_employee_not_found():
    response = client.delete("/employees/EMP99999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Employee not found"
    }

def test_update_employee_not_found():
    updated_data = {
        "name": "Neha Updated",
        "email": "neha.updated@example.com",
        "department": "HR",
        "salary": 45000,
        "age": 28,
        "location": "Hyderabad"
    }

    response = client.put(
        "/employees/EMP99999",
        json=updated_data
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Employee not found"
    }
