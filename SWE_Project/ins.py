import sqlite3


def create_table():
    conn = sqlite3.connect('instructor_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS instructor (
            instructor_name TEXT,
            email TEXT,
            phone TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_query(instructor_name, email, phone, password):
    conn = sqlite3.connect('instructor_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO queries (instructor_name, email, phone, password) 
        VALUES (?, ?, ?, ?)
    ''', (instructor_name, email, phone, password))  # الاستفسار يبدأ بدون رد
    conn.commit()
    conn.close()

def update_instructor_info(instructor_name=None, email=None, phone=None, password=None):
    conn = sqlite3.connect('instructor_data.db')
    c = conn.cursor()

    if not any([instructor_name, email, phone, password]):

        return
    c.execute("SELECT * FROM instructor LIMIT 1")
    current_data = c.fetchone()
    if not current_data:

        return

    updated_name = instructor_name if instructor_name else current_data[0]
    updated_email = email if email else current_data[1]
    updated_phone = phone if phone else current_data[2]
    updated_password = password if password else current_data[3]
    c.execute('''
        UPDATE instructor
        SET instructor_name = ?, email = ?, phone = ?, password = ?
    ''', (updated_name, updated_email, updated_phone, updated_password))

    conn.commit()
    conn.close()

def get_instructor_data():

    conn = sqlite3.connect('instructor_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM instructor")
    result = c.fetchone()


    conn.close()

    return result


def check_and_insert_instructor(name, email, phone, password):
    conn = sqlite3.connect('instructor_data.db')
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM instructor WHERE instructor_name = ?", (name,))
    count = c.fetchone()[0]

    if count == 0:
        c.execute('''
            INSERT INTO instructor (instructor_name, email, phone, password)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, password))
        conn.commit()
    conn.close()
create_table()
check_and_insert_instructor("Sarah Zahran", "sarazahran@gmail.com", "01550858816", "sarah123")
