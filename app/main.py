
from db_connection import get_connection


# 1. REGISTER EMPLOYEE - CREATE

def register_employee():

    employee_id = input("Enter Employee ID: ").strip()
    name = input("Enter Employee Name: ").strip()
    email = input("Enter Employee Email: ").strip()
    department = input("Enter Department: ").strip()

    while True:
        try:
            salary = float(input("Enter Salary: "))
            if salary > 0:
                break
            print("Salary must be greater than zero.")
        except ValueError:
            print("Enter a valid salary.")

    while True:
        try:
            age = int(input("Enter Age: "))
            if age > 0:
                break
            print("Age must be greater than zero.")
        except ValueError:
            print("Enter a valid age.")

    location = input("Enter Location: ").strip()

    connection = None
    cursor = None

    try:
        connection = get_connection()
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
        print("Employee registered successfully!")

    except Exception as error:
        if connection:
            connection.rollback()
        print("Registration failed:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 2. VIEW EMPLOYEES - READ

def view_employees():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM employees")

        employees = cursor.fetchall()

        if not employees:
            print("No employee records found.")
            return

        for employee in employees:
            print("\n-----------------------------")
            print("Employee ID:", employee[0])
            print("Name:", employee[1])
            print("Email:", employee[2])
            print("Department:", employee[3])
            print("Salary:", employee[4])
            print("Age:", employee[5])
            print("Location:", employee[6])

    except Exception as error:
        print("Error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 3. SEARCH EMPLOYEE - READ BY ID

def search_employee():

    employee_id = input("Enter Employee ID to search: ").strip()

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM employees WHERE employee_id = %s",
            (employee_id,)
        )

        employee = cursor.fetchone()

        if employee:
            print("\nEmployee Found!")
            print("Employee ID:", employee[0])
            print("Name:", employee[1])
            print("Email:", employee[2])
            print("Department:", employee[3])
            print("Salary:", employee[4])
            print("Age:", employee[5])
            print("Location:", employee[6])
        else:
            print("Employee not found.")

    except Exception as error:
        print("Search failed:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 4. UPDATE EMPLOYEE - UPDATE

def update_employee():

    employee_id = input("Enter Employee ID to update: ").strip()

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT employee_id FROM employees WHERE employee_id = %s",
            (employee_id,)
        )

        employee = cursor.fetchone()

        if not employee:
            print("Employee not found.")
            return

        print("\nEmployee Found!")
        print("1. Name")
        print("2. Email")
        print("3. Department")
        print("4. Salary")
        print("5. Age")
        print("6. Location")

        choice = input("Which detail do you want to update? ")

        fields = {
            "1": ("name", "Enter new name: "),
            "2": ("email", "Enter new email: "),
            "3": ("department", "Enter new department: "),
            "4": ("salary", "Enter new salary: "),
            "5": ("age", "Enter new age: "),
            "6": ("location", "Enter new location: ")
        }

        if choice not in fields:
            print("Invalid choice.")
            return

        column, message = fields[choice]

        if choice == "4":
            while True:
                try:
                    new_value = float(input(message))
                    if new_value > 0:
                        break
                    print("Salary must be greater than zero.")
                except ValueError:
                    print("Enter a valid salary.")

        elif choice == "5":
            while True:
                try:
                    new_value = int(input(message))
                    if new_value > 0:
                        break
                    print("Age must be greater than zero.")
                except ValueError:
                    print("Enter a valid age.")

        else:
            new_value = input(message).strip()

        cursor.execute(
            f"UPDATE employees SET {column} = %s WHERE employee_id = %s",
            (new_value, employee_id)
        )

        connection.commit()

        print("Employee details updated successfully!")

    except Exception as error:
        if connection:
            connection.rollback()
        print("Update failed:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 5. DELETE EMPLOYEE - DELETE


def delete_employee():
    connection = None
    cursor = None

    try:
        employee_id = input("Enter Employee ID to delete: ").strip()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM employees WHERE employee_id = %s",
            (employee_id,)
        )

        employee = cursor.fetchone()

        if employee is None:
            print("Employee not found.")
            return

        print("\nEmployee found:")
        print("ID:", employee[0])
        print("Name:", employee[1])
        print("Email:", employee[2])
        print("Department:", employee[3])

        confirmation = input(
            "Are you sure you want to delete this employee? (yes/no): "
        ).strip().lower()

        if confirmation == "yes":
            cursor.execute(
                "DELETE FROM employees WHERE employee_id = %s",
                (employee_id,)
            )
            connection.commit()
            print("Employee deleted successfully.")
        else:
            print("Deletion cancelled.")

    except Exception as error:
        if connection:
            connection.rollback()
        print("Error deleting employee:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# 6. MAIN MENU

while True:

    print("\n===== EMPLOYEE MANAGEMENT SYSTEM =====")
    print("1. Register Employee")
    print("2. View Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        register_employee()

    elif choice == "2":
        view_employees()

    elif choice == "3":
        search_employee()

    elif choice == "4":
        update_employee()

    elif choice == "5":
        delete_employee()

    elif choice == "6":
        print("Exiting Employee Management System.")
        break

    else:
        print("Invalid choice. Please try again.")
