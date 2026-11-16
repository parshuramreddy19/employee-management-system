from db_connection import get_connection


def view_employees():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM employees")

        employees = cursor.fetchall()

        if not employees:
            print("No employee records found.")

        else:
            for employee in employees:
                print("\nEmployee ID:", employee[0])
                print("Name:", employee[1])
                print("Email:", employee[2])
                print("Department:", employee[3])
                print("Salary:", employee[4])
                print("Age:", employee[5])
                print("Location:", employee[6])

        cursor.close()

    except Exception as error:
        print("Error:", error)

    finally:
        connection.close()


view_employees()