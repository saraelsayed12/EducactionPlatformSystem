import sqlite3



def create_student_table():

    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,  
        phone_number TEXT,
        password TEXT
    )
    ''')
    conn.commit()
    conn.close()

def add_student(name, email, phone_number, password):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()


    c.execute('SELECT * FROM students WHERE email = ?', (email,))
    existing_student = c.fetchone()

    if existing_student:
        conn.close()
        return False


    c.execute('''
        INSERT INTO students (name, email, phone_number, password) 
        VALUES (?, ?, ?, ?)
    ''', (name, email, phone_number, password))
    conn.commit()
    conn.close()
    return True



def register_student(name, email, phone_number, password, confirm_password):
    if password != confirm_password:
        return "Passwords do not match"


    success = add_student(name, email, phone_number, password)
    if success:
        return "Student registered successfully"
    else:
        return "Email is already registered"


def fetch_students_from_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, email, phone_number,password FROM students")
    students = cursor.fetchall()
    conn.close()
    return students


def update_student_info_db(name, new_name=None, email=None, phone=None, password=None):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()


    if not any([new_name, email, phone, password]):
        print("No data to update.")
        return


    c.execute('SELECT * FROM students WHERE name = ?', (name,))
    current_data = c.fetchone()

    if not current_data:
        print(f"No student found with name: {name}")
        conn.close()
        return


    updated_name = new_name if new_name else current_data[0]
    updated_email = email if email else current_data[1]
    updated_phone = phone if phone else current_data[2]
    updated_password = password if password else current_data[3]


    try:
        c.execute('''
            UPDATE students 
            SET name = ?, email = ?, phone_number = ?, password = ?
            WHERE name = ?
        ''', (updated_name, updated_email, updated_phone, updated_password, name))
        conn.commit()
        print(f"Student '{name}' updated successfully!")
    except sqlite3.Error as e:
        print(f"Error updating student: {e}")
    finally:
        conn.close()
create_student_table()
add_student('sara', 'si@gmail.com', '12345678901','s@gmail.com')
li= fetch_students_from_db()
print(li)