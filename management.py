import mysql.connector as sql

# --- Database Connection ---
try:
    conn = sql.connect(host='localhost', user='root',
                       passwd='admin@123', database='hostel_management')
    conn.autocommit = True
    if conn.is_connected():
        print('Connected to database successfully!')
    else:
        print('Could not connect to the database.')
        exit() # Exit if connection fails

except sql.Error as err:
    print(f"Error connecting to database: {err}")
    exit() # Exit if connection fails

cl = conn.cursor()

# --- Create Table (if it doesn't exist) ---
try:
    cl.execute("""
        CREATE TABLE IF NOT EXISTS hostel_management (
            roll_no INT PRIMARY KEY,
            name VARCHAR(50),
            address VARCHAR(255),
            room_no INT,
            dept VARCHAR(20),
            fees INT,
            bal INT
        )
    """)
    print("Table 'hostel_management' checked/created successfully.")
except sql.Error as err:
    print(f"Error creating table: {err}")
    conn.close()
    exit()

# --- Main Menu Loop ---
while True:
    print("\n--- WELCOME TO HOSTEL MANAGEMENT ---")
    print("1. ADMISSION FORM")
    print("2. FEE CHECKING")
    print("3. MODIFY/VIEW STUDENT DATA")
    print("4. EXIT")

    try:
        choice = int(input('ENTER YOUR CHOICE: '))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4.")
        continue

    # --- Choice 1: Admission Form ---
    if choice == 1:
        try:
            v_roll = int(input("ENTER YOUR ROLL NUMBER: "))
            v_name = input("ENTER YOUR NAME: ")
            v_add = input("ENTER YOUR ADDRESS: ")
            v_room_no = int(input("ENTER YOUR ROOM NUMBER: "))
            v_dept = input("ENTER YOUR DEPARTMENT: ")
            v_fees = int(input("ENTER YOUR FEES: "))
            v_bal = int(input("ENTER YOUR BALANCE: "))

            # Using parameterized query to prevent SQL injection
            insert_query = """
                INSERT INTO hostel_management (roll_no, name, address, room_no, dept, fees, bal)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            data_to_insert = (v_roll, v_name, v_add, v_room_no, v_dept, v_fees, v_bal)

            cl.execute(insert_query, data_to_insert)
            # conn.commit() is not needed here if autocommit is True, but good practice if it wasn't.
            print("Student admitted successfully!")
        except ValueError:
            print("Invalid input. Please ensure numeric fields are numbers.")
        except sql.Error as err:
            print(f"Error admitting student: {err}")

    # --- Choice 2: Fee Checking ---
    elif choice == 2:
        print("\nAVAILABLE DEPARTMENTS AS FOLLOWS:")
        print("1. COMPUTER")
        print("2. BIO")
        print("3. TECH")
        print("4. PHYSICS")
        print("5. ECO")
        print("6. ENG")
        department = input("ENTER THE DEPARTMENT to check fees for: ").upper() # Convert to uppercase for consistent comparison

        try:
            # Modified to fetch fees for students in a given department
            # If you have a separate 'fees' table, you'd need to join or query that table
            select_fees_query = "SELECT SUM(fees - bal) AS total_collection, AVG(fees) AS avg_fees FROM hostel_management WHERE dept = %s"
            cl.execute(select_fees_query, (department,))
            data = cl.fetchone()

            if data and data[1] is not None: # Check if any data was returned and avg_fees is not None
                print(f"For department '{department}':")
                print(f"  Total collected fees: {data[0] if data[0] is not None else 0}")
                print(f"  Average fees: {data[1]:.2f}")
            else:
                print(f"No students found in department '{department}' or no fee data available.")
        except sql.Error as err:
            print(f"Error checking fees: {err}")

    # --- Choice 3: Modify/View Student Data ---
    elif choice == 3:
        try:
            roll_no = int(input("ENTER THE ROLL NUMBER to view/modify: "))
            select_query = "SELECT * FROM hostel_management WHERE roll_no = %s"
            cl.execute(select_query, (roll_no,))
            data = cl.fetchone() # Use fetchone() for a single record

            if data:
                print("\n--- Student Details ---")
                print(f"Roll No: {data[0]}")
                print(f"Name: {data[1]}")
                print(f"Address: {data[2]}")
                print(f"Room No: {data[3]}")
                print(f"Department: {data[4]}")
                print(f"Fees: {data[5]}")
                print(f"Balance: {data[6]}")

                # Optional: Add functionality to modify data
                modify_choice = input("Do you want to modify this student's data? (yes/no): ").lower()
                if modify_choice == 'yes':
                    print("\n--- Select field to modify ---")
                    print("1. Name")
                    print("2. Address")
                    print("3. Room Number")
                    print("4. Department")
                    print("5. Fees")
                    print("6. Balance")
                    modify_field_choice = input("Enter your choice (1-6): ")

                    update_value = None
                    update_column = None

                    if modify_field_choice == '1':
                        update_column = 'name'
                        update_value = input("Enter new name: ")
                    elif modify_field_choice == '2':
                        update_column = 'address'
                        update_value = input("Enter new address: ")
                    elif modify_field_choice == '3':
                        update_column = 'room_no'
                        update_value = int(input("Enter new room number: "))
                    elif modify_field_choice == '4':
                        update_column = 'dept'
                        update_value = input("Enter new department: ")
                    elif modify_field_choice == '5':
                        update_column = 'fees'
                        update_value = int(input("Enter new fees: "))
                    elif modify_field_choice == '6':
                        update_column = 'bal'
                        update_value = int(input("Enter new balance: "))
                    else:
                        print("Invalid modification choice.")
                        continue

                    if update_column and update_value is not None:
                        update_query = f"UPDATE hostel_management SET {update_column} = %s WHERE roll_no = %s"
                        cl.execute(update_query, (update_value, roll_no))
                        print("Data updated successfully!")
            else:
                print(f"No student found with roll number {roll_no}.")
        except ValueError:
            print("Invalid input. Please enter a valid roll number.")
        except sql.Error as err:
            print(f"Error accessing/modifying data: {err}")

    # --- Choice 4: Exit ---
    elif choice == 4:
        print("QUITTING!!!!!!!!!")
        break
    else:
        print("Invalid choice. Please select a number between 1 and 4.")

# --- Close Connection ---
if conn.is_connected():
    cl.close()
    conn.close()
    print("Database connection closed.")