import sqlite3

class CoursesDatabase:
    def __init__(self, db_name="courses.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON;')
        self.create_table()

        self.cursor.execute('PRAGMA foreign_keys = ON;')

    def create_table(self):

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            course_name TEXT NOT NULL,
            video_link TEXT,
            pdf_link TEXT
        )
        ''')


        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY,
            course_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
        )
        ''')

        # إنشاء جدول لإجابات الكويزات إذا لم يكن موجودًا
        self.cursor.execute('''
         CREATE TABLE IF NOT EXISTS quiz_answers (
             id INTEGER PRIMARY KEY,
             quiz_id INTEGER NOT NULL,
             student_id INTEGER NOT NULL,
             student_answer TEXT NOT NULL,
             is_answer_correct INTEGER NOT NULL DEFAULT 0,
             FOREIGN KEY (quiz_id) REFERENCES quizzes (id)
             FOREIGN KEY (student_id) REFERENCES students (id)
         )
         ''')
        self.connection.commit()

    def add_course(self, course_name, video_link=None, pdf_link=None):

        self.cursor.execute(''' 
            INSERT INTO courses (course_name, video_link, pdf_link)
            VALUES (?, ?, ?)
        ''', (course_name, video_link or '', pdf_link or ''))
        self.connection.commit()

        return self.cursor.lastrowid

    def add_quiz(self, course_id, question, correct_answer):
        if not course_id:
            print("Error: course_id cannot be None.")
            return
        try:

            self.cursor.execute('''
                INSERT INTO quizzes (course_id, question, correct_answer)
                VALUES (?, ?, ?)
            ''', (course_id, question, correct_answer))
            self.connection.commit()
            print("Quiz added successfully.")
        except Exception as e:
            print(f"Error adding quiz: {e}")
            self.connection.rollback()

    def submit_answer(self, quiz_id, student_id, student_answer):
        try:

            self.cursor.execute("SELECT correct_answer FROM quizzes WHERE id = ?", (quiz_id,))
            correct_answer = self.cursor.fetchone()

            if correct_answer:
                correct_answer = correct_answer[0]
                is_correct = 1 if student_answer.strip().lower() == correct_answer.strip().lower() else 0


                self.cursor.execute('''
                    INSERT INTO quiz_answers (quiz_id, student_id, student_answer, is_answer_correct)
                    VALUES (?, ?, ?, ?)
                ''', (quiz_id, student_id, student_answer, is_correct))
                self.connection.commit()


                if is_correct:
                    print("الإجابة صحيحة!")
                else:
                    print("الإجابة خاطئة!")
            else:
                print("Not Exist")
                return
        except Exception as e:
            print(f"Error submitting answer: {e}")
            self.connection.rollback()

    def get_correct_answer(self, quiz_id):
       try:
             self.cursor.execute("SELECT correct_answer FROM quizzes WHERE id = ?", (quiz_id,))
             result = self.cursor.fetchone()
             return result[0] if result else "No answer available"
       except Exception as e:
             print(f"Error fetching correct answer: {e}")
             return "Error"

    def get_courses(self):

        self.cursor.execute(
            "SELECT id, course_name, video_link, pdf_link FROM courses")
        courses = self.cursor.fetchall()
        return courses
    def update_course(self, course_id, course_name=None, video_link=None, pdf_link=None):
        query = 'UPDATE courses SET '
        params = []

        if course_name is not None:
            query += 'course_name = ?, '
            params.append(course_name)
        if video_link is not None:
            query += 'video_link = ?, '
            params.append(video_link)
        if pdf_link is not None:
            query += 'pdf_link = ?, '
            params.append(pdf_link)
        query = query.rstrip(', ')
        query += ' WHERE id = ?'
        params.append(course_id)

        try:
            self.cursor.execute(query, tuple(params))
            self.connection.commit()
            print("Course updated successfully.")
        except Exception as e:
            print(f"Error updating course: {e}")
            self.connection.rollback()

    def delete_course(self, course_id):

        self.cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
        course = self.cursor.fetchone()
        if not course:
            print("Error: Course not found.")
            return


        self.cursor.execute('DELETE FROM quizzes WHERE course_id = ?', (course_id,))
        self.connection.commit()


        self.cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        self.connection.commit()
        print("Course and related quizzes deleted successfully.")


        self.cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        self.connection.commit()
        print("Course deleted successfully.")

    def get_course_by_id(self, course_id):
        try:
            self.cursor.execute("SELECT * FROM courses WHERE id=?", (course_id,))
            course = self.cursor.fetchone()
            return course
        except Exception as e:
            print(f"Error fetching course by ID: {e}")
            return None

    def get_quizzes(self, course_id):
        try:
            self.cursor.execute("SELECT id, question FROM quizzes WHERE course_id = ?", (course_id,))
            quizzes = self.cursor.fetchall()
            return quizzes if quizzes else []
        except Exception as e:
            print(f"Error fetching quizzes: {e}")
            return []

    def close(self):

        self.connection.close()