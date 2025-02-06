import sqlite3

def create_table():
    conn = sqlite3.connect('student_queries.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            student_name TEXT,
            query TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_query(student_name, query):
    conn = sqlite3.connect('student_queries.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO queries (student_name, query, response) 
        VALUES (?, ?, ?)
    ''', (student_name, query, None))  # الاستفسار يبدأ بدون رد
    conn.commit()
    conn.close()


def get_unanswered_queries():
    conn = sqlite3.connect('student_queries.db')
    c = conn.cursor()
    c.execute('SELECT * FROM queries WHERE response IS NULL')
    queries = c.fetchall()
    conn.close()
    return queries


def update_response(query_text, response_text):
    conn = sqlite3.connect('student_queries.db')
    c = conn.cursor()
    c.execute('''
        UPDATE queries 
        SET response = ? 
        WHERE query = ?
    ''', (response_text, query_text))
    conn.commit()
    conn.close()

def get_answered_queries(student_name):

    conn = sqlite3.connect('student_queries.db')
    c = conn.cursor()
    c.execute("SELECT query, response FROM queries WHERE student_name = ? AND response IS NOT NULL", (student_name,))
    queries = c.fetchall()
    conn.close()
    return queries
