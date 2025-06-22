*Hostel Management System*

A command-line interface (CLI) application developed in Python to manage student admissions, fees, and data within a hostel environment using a MySQL database.


*🚀 Features*

Student Admissions: Easily add new students to the hostel with details like roll number, name, address, room number, department, fees, and balance.

Fee Checking: View fee information, including total collected fees and average fees, for students grouped by department.

Student Data Management: Search for students by their roll number to view their complete details and optionally modify their information (name, address, room number, department, fees, balance).

Persistent Data Storage: All student and fee data is securely stored in a MySQL database, ensuring data integrity and persistence.

User-Friendly CLI: Simple menu-driven interface for easy navigation and operation.


*🛠️ Technologies Used*

Python : The core programming language for the application logic.

MySQL Database: Used for robust data storage and retrieval.

`mysql-connector-python`: Python library to facilitate communication between Python and MySQL.


*How it works*

Once the application is running, you'll see a main menu:

--- WELCOME TO HOSTEL MANAGEMENT ---
1. ADMISSION FORM
2. FEE CHECKING
3. MODIFY/VIEW STUDENT DATA
4. EXIT
   
ENTER YOUR CHOICE:

To Add a Student: Enter 1 and follow the prompts to input student details.

To Check Fees: Enter 2 and specify the department to see fee statistics.

To View/Modify Student Data: Enter 3, provide the student's roll number, and choose whether to view or modify their record.

To Exit: Enter 4.
