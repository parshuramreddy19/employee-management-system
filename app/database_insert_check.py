from db_connection import get_connection


def insert_employee():

    employee_id = input("Enter Employee ID: ")
    name = input("Enter Employee Name: ")
    email = input("Enter Email: ")
    department = input("Enter Department: ")
    salary = float(input("Enter Salary: "))
    age = int(input("Enter Age: "))
    location = input("Enter Location: ")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO employees
            (employee_id, name, email, department, salary, age, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (employee_id, name, email, department, salary, age, location)
        )

        connection.commit()

        print("Employee saved successfully in PostgreSQL!")

        cursor.close()

    except Exception as error:
        connection.rollback()
        print("Error:", error)

    finally:
        connection.close()


insert_employee()