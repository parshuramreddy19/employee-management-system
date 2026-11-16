from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, HTTPException
from psycopg.errors import UniqueViolation
from app.db_connection import get_connection

app = FastAPI(title="Employee Management API")

class Employee(BaseModel):
    employee_id: str = Field(pattern=r"^EMP\d+$")
    name: str = Field(min_length=2)
    email: EmailStr
    department: str
    salary: float = Field(gt=0)
    age: int = Field(gt=0, le=100)
    location: str


class EmployeeUpdate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    department: str
    salary: float = Field(gt=0)
    age: int = Field(gt=0, le=100)
    location: str


@app.get("/")
def home():
    return {"message": "Employee Management API is running"}


@app.get("/employees")
def get_all_employees():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM employees")

        employees = cursor.fetchall()

        columns = [column.name for column in cursor.description]

        employee_list = [
            dict(zip(columns, employee))
            for employee in employees
        ]

        return employee_list

    except Exception as error:
        print("Error:", error)
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve employees"
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.post("/employees")
def register_employee(employee: Employee):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO employees
            (employee_id, name, email, department, salary, age, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING employee_id
            """,
            (
                employee.employee_id,
                employee.name,
                employee.email,
                employee.department,
                employee.salary,
                employee.age,
                employee.location
            )
        )

        new_employee = cursor.fetchone()
        connection.commit()

        return {
            "message": "Employee registered successfully",
            "employee_id": new_employee[0]
        }

    except UniqueViolation as error:
        connection.rollback()

        if error.diag.constraint_name == "employees_pkey":
            raise HTTPException(
                status_code=409,
                detail="Employee ID already exists"
            )

        elif error.diag.constraint_name == "employees_email_key":
            raise HTTPException(
                status_code=409,
                detail="Email address already exists"
            )

        raise HTTPException(
            status_code=409,
            detail="Duplicate employee record"
        )

    except Exception as error:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to register employee"
        )

    finally:
        cursor.close()
        connection.close()
@app.get("/employees/{employee_id}")
def get_employee_by_id(employee_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT * FROM employees
            WHERE employee_id = %s
            """,
            (employee_id,)
        )

        employee = cursor.fetchone()

        if employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        columns = [description[0] for description in cursor.description]

        return dict(zip(columns, employee))

    finally:
        cursor.close()
        connection.close()
@app.put("/employees/{employee_id}")
def update_employee(employee_id: str, employee: EmployeeUpdate):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE employees
            SET name = %s,
                email = %s,
                department = %s,
                salary = %s,
                age = %s,
                location = %s
            WHERE employee_id = %s
            RETURNING employee_id
        """

        values = (
            employee.name,
            employee.email,
            employee.department,
            employee.salary,
            employee.age,
            employee.location,
            employee_id
        )

        cursor.execute(query, values)

        updated_employee = cursor.fetchone()

        if updated_employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        connection.commit()

        return {
            "message": "Employee updated successfully",
            "employee_id": updated_employee[0]
        }

    except HTTPException:
        raise

    except Exception as error:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM employees WHERE employee_id = %s RETURNING employee_id",
            (employee_id,)
        )

        deleted_employee = cursor.fetchone()

        if deleted_employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        connection.commit()

        return {
            "message": "Employee deleted successfully",
            "employee_id": deleted_employee[0]
        }

    except HTTPException:
        raise

    except Exception as error:
        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
