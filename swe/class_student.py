import tkinter as tk
from tkinter import messagebox
import json
import re
import os
import webbrowser
from PIL import Image, ImageTk
import database_query
import sqlite3
import webbrowser
from courses_database import CoursesDatabase

db = CoursesDatabase()
import student_database
import class_instructorApp
import ins

ins.create_table()


class EducationalPlatform:
    def __init__(self, root):
        self.root = root
        self.root.title("Educational Platform")
        self.root.geometry("800x600")
        self.root.configure(bg="#f8c9d8")  # Changing background color to pink
        self.db = CoursesDatabase()
        self.db_name = 'students.db'

        self.student_details = list()
        student_database.create_student_table()

        self.logged_in_user = None

        self.role_selection_screen()
        self.quiz_scores = []

    def create_student_table(self):

        """Ensure the students table exists in the database"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,  -- استخدم UNIQUE بدلاً من PRIMARY KEY هنا
            phone_number TEXT,
            password TEXT
        )
        ''')
        conn.commit()
        conn.close()

    def update_student_info_db(self, name, new_name=None, email=None, phone=None, password=None):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()

        # التحقق إذا كانت هناك بيانات جديدة للتحديث
        if not any([new_name, email, phone, password]):
            print("No data to update.")
            return

        # التحقق من وجود الطالب بناءً على الاسم
        c.execute('SELECT * FROM students WHERE name = ?', (name,))
        current_data = c.fetchone()

        if not current_data:
            print(f"No student found with name: {name}")
            conn.close()
            return

        # تحديث القيم
        updated_name = new_name if new_name else current_data[0]
        updated_email = email if email else current_data[1]
        updated_phone = phone if phone else current_data[2]
        updated_password = password if password else current_data[3]

        # تحديث بيانات الطالب في قاعدة البيانات
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

    def role_selection_screen(self):
        self.clear_screen()
        image_path = os.path.join(os.path.dirname(__file__), "g.jpg")
        self.image = Image.open(image_path)
        self.image = self.image.resize((900, 700), Image.Resampling.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_label = tk.Label(self.root, image=self.image_tk)
        self.image_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_style = {"font": ("Comic Sans MS", 12, "bold"), "width": 40, "bg": "#ECF0F1", "fg": "blue"}

        tk.Label(self.root, text="☸ Welcome to the platform ☸", font=("Comic Sans MS", 20, "bold"), bg="gold",
                 fg="blue").pack(pady=50)

        # استخدام pack للأزرار بعد العنوان مباشرة
        tk.Button(self.root, text="Student", **button_style, command=self.login_screen).pack(pady=20)
        tk.Button(self.root, text="Instructor", **button_style, command=self.login_screen_ins).pack(pady=20)

    def instructor_dashboard(self):
        class_instructorApp.InstructorApp(self.root)  # هنا يتم تمرير نافذة جديدة لفتح واجهة المدرس

    def login_screen_ins(self):
        self.clear_screen()


        tk.Label(self.root, text="Login", font=("Comic Sans MS", 20, "bold"), bg="#f8c9d8").pack(
            pady=20)
        tk.Label(self.root, text="Email:", font=("Arial", 15, "bold"), bg="#f8c9d8").pack(
            pady=20)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=("Arial", 15, "bold"), bg="#f8c9d8").pack(
            pady=20)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login_ins, bg="#ff0000", fg="white", width=15).pack(
            pady=10)  # تغيير لون الزر إلى الأحمر

        tk.Button(self.root, text="Back to Role section", command=self.role_selection_screen, bg="#ff0000", fg="white",
                  width=15).pack(pady=10)

    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Arial", 18), bg="#f8c9d8").pack(pady=20)

        tk.Label(self.root, text="Email:", bg="#f8c9d8").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", bg="#f8c9d8").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="Login", command=self.login, bg="white", fg="blue",
                  font=("Arial", 14), width=15).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register_screen, bg="white", fg="blue",
                  font=("Arial", 14), width=15).pack(pady=10)
        tk.Button(self.root, text="Back to Role section", command=self.role_selection_screen, bg="white", fg="blue",
                  font=("Arial", 14), width=15).pack(pady=10)

    def register_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Register", font=("Arial", 18), bg="#f8c9d8").pack(pady=20)

        tk.Label(self.root, text="Name:", bg="#f8c9d8").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Email:", bg="#f8c9d8").pack()
        self.reg_email_entry = tk.Entry(self.root)
        self.reg_email_entry.pack(pady=5)

        tk.Label(self.root, text="Phone Number:", bg="#f8c9d8").pack()
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", bg="#f8c9d8").pack()
        self.reg_password_entry = tk.Entry(self.root, show="*")
        self.reg_password_entry.pack(pady=5)

        tk.Label(self.root, text="Confirm Password:", bg="#f8c9d8").pack()
        self.confirm_password_entry = tk.Entry(self.root, show="*")
        self.confirm_password_entry.pack(pady=5)

        tk.Button(self.root, text="Register", command=self.register, bg="white", fg="blue",
                  font=("Arial", 14), width=20).pack(pady=10)
        tk.Button(self.root, text="Back to login", command=self.login_screen, bg="white", fg="blue",
                  font=("Arial", 14), width=20).pack(pady=10)
        tk.Button(self.root, text="Back to Role section", command=self.role_selection_screen, bg="white", fg="blue",
                  font=("Arial", 14), width=20).pack(pady=10)

    # دالة التسجيل
    def register(self):
        name = self.name_entry.get()
        email = self.reg_email_entry.get()
        phone_number = self.phone_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not name or not email or not phone_number or not password:
            messagebox.showerror("Register", "Please fill in all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Register", "Passwords do not match.")
            return

            # Check if the email is already registered in the database
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM students WHERE email = ?', (email,))
        existing_user = c.fetchone()

        if existing_user:
            messagebox.showerror("Register", "Email already registered.")
        else:
            # Register the new user in the database
            c.execute('''INSERT INTO students (name, email, phone_number, password) 
                            VALUES (?, ?, ?, ?)''', (name, email, phone_number, password))
            conn.commit()
            messagebox.showinfo("Register", "Registration successful!")
            self.login_screen()
    # دالة تسجيل الدخول
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if not email or not password:
            messagebox.showerror("Login", "Please enter both email and password.")
            return
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('SELECT * FROM students WHERE email = ? AND password = ?', (email, password))
        user = c.fetchone()


        if user:
            self.student_details = list(user)


            self.main_menu()
        else:
            messagebox.showerror("Login", "Invalid email or password.")

        conn.close()

    def login_ins(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        ans = ins.get_instructor_data()
        if email == ans[1] and ans[3] == password:
            self.instructor_dashboard()
        else:
            messagebox.showerror("Login", "Invalid email or password.")

    def show_Student_info(self):
        self.clear_screen()
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(self.root, text="👨‍🏫 My Information 👨‍🏫", font=("Comic Sans MS", 20, "bold"), bg="#f8c9d8").pack(
            pady=20)
        infoo = self.student_details

        tk.Label(self.root, text=f"Name : {infoo[1]}", font=("Arial", 15, "bold"), bg="#f8c9d8").pack(
            pady=20)
        tk.Label(self.root, text=f"Email : {infoo[2]}", font=("Arial", 15, "bold"), bg="#f8c9d8").pack(
            pady=20)
        tk.Label(self.root, text=f"Phone : {infoo[3]}", font=("Arial", 15, "bold"), bg="#f8c9d8").pack(
            pady=20)
        tk.Label(self.root, text=f"Password : {infoo[4]}", font=("Arial", 15, "bold"), bg="#f8c9d8").pack(
            pady=20)

        tk.Button(self.root, text="Update Information", command=self.update_info, bg="#4CAF50", fg="white",
                  font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(self.root, text="Back to Home", command=self.main_menu, bg="#ff7f50", fg="white",
                  font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(self.root, text="Exit ✌", command=self.root.quit, bg="#ff6666", fg="white",
                  font=("Arial", 14, "bold")).pack(pady=10)

    def create_entry(self, parent, label_text, default_value, show=None):
        tk.Label(parent, text=label_text, font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        entry = tk.Entry(parent, width=30, show=show)
        entry.insert(0, default_value)
        entry.pack(pady=5)
        return entry

    def update_info(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Information")
        update_window.geometry("400x600")
        update_window.configure(bg="#f0f8ff")

        tk.Label(update_window, text="Update Your Information", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        ans = self.student_details
        name_entry = self.create_entry(update_window, "Name:", ans[1])
        email_entry = self.create_entry(update_window, "Email:", ans[2])
        password_entry = self.create_entry(update_window, "Password:", ans[4], show="*")
        phone_entry = self.create_entry(update_window, "Phone:", ans[3])

        def validate_and_update():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            phone = phone_entry.get()

            # التحقق من صحة المدخلات
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror("Error", "Invalid email format!")
                return
            if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]",
                                                                                       password) or not re.search(r"\d",
                                                                                                                  password):
                messagebox.showerror("Error",
                                     "Password must be at least 8 characters long, include uppercase, lowercase, and a number!")
                return
            if not phone.isdigit() or len(phone) != 11:
                messagebox.showerror("Error", "Phone number must be 11 digits long and contain only numbers!")
                return

            self.update_student_info_db(ans[0], name, email, phone, password)

            self.student_details[1]= name
            self.student_details[2] = email

            self.student_details[3] =phone
            self.student_details[4] =password


            # إغلاق نافذة التحديث
            messagebox.showinfo("Success", "Information updated successfully!")
            update_window.destroy()

            # إعادة عرض المعلومات المحدثة
            self.show_Student_info()

        tk.Button(update_window, text="Save Changes", command=validate_and_update, bg="#4CAF50", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=20)
        tk.Button(update_window, text="Cancel", command=update_window.destroy, bg="#f44336", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=5)

    def main_menu(self):
        self.clear_screen()

        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
        button_style = {"font": ("Comic Sans MS", 12, "bold"), "width": 40, "bg": "#ECF0F1", "fg": "blue"}

        tk.Label(self.root, text="☸ Home page ☸", font=("Comic Sans MS", 20, "bold"), bg="#f8c9d8", fg="blue").pack(pady=50)

        tk.Button(self.root, text="show Info", command=self.show_Student_info, bg="white", fg="blue",
                  font=("Arial", 12), width=20).pack(pady=15)
        tk.Button(self.root, text="View All My Courses", command=self.view_courses, bg="white", fg="blue",
                  font=("Arial", 12), width=20).pack(pady=15)


        tk.Button(self.root, text="Contact Teacher", command=self.contact_instructor, bg="white", fg="blue",
                  font=("Arial", 12), width=20).pack(pady=15)
        tk.Button(self.root, text="Logout", command=self.logout, bg="white", fg="blue", font=("Arial", 12),
                  width=20).pack(pady=15)

    def view_courses(self):
        self.clear_screen()

        tk.Label(self.root, text="Available Courses", font=("Arial", 20), bg="#f8c9d8").pack(pady=20)

        courses = self.db.get_courses()  # استرجاع الكورسات من قاعدة البيانات

        for course in courses:
            course_id, course_name, video_link, pdf_link = course
            tk.Button(self.root, text=course_name, command=lambda c_id=course_id: self.view_course_details(c_id),
                      bg="#ff0000", fg="white", width=30).pack(pady=5)

        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, bg="#ff0000", fg="white", width=15).pack(
            pady=10)

    def view_course_details(self, course_id):
        self.clear_screen()

        # استرجاع بيانات الكورس من قاعدة البيانات
        course = self.db.get_course_by_id(course_id)
        if not course:
            tk.Label(self.root, text="Course not found", font=("Arial", 18), bg="#f8c9d8").pack(pady=20)
            return

        # فك تجميع القيم
        course_id, course_name, video_link, pdf_link = course

        tk.Label(self.root, text=f"Course: {course_name}", font=("Arial", 18), bg="#f8c9d8").pack(pady=20)

        # زر مشاهدة الفيديو
        if video_link:
            tk.Button(self.root, text="View Video", command=lambda: self.view_video(video_link), bg="#ff0000",
                      fg="white", width=20).pack(pady=5)
        else:
            tk.Label(self.root, text="No video available", font=("Arial", 12), bg="#f8c9d8").pack(pady=5)

        # زر تحميل PDF
        if pdf_link:
            tk.Button(self.root, text="View PDF", command=lambda: self.view_pdf(pdf_link), bg="#ff0000", fg="white",
                      width=20).pack(pady=5)
        else:
            tk.Label(self.root, text="No PDF available", font=("Arial", 12), bg="#f8c9d8").pack(pady=5)

        # عرض الكويزات (إذا كانت موجودة)
        quizzes = self.db.get_quizzes(course_id)
        if quizzes:
            tk.Button(self.root, text="Take Quiz", command=lambda: self.take_quiz(course_id), bg="#ff0000", fg="white",
                      width=20).pack(pady=5)
        else:
            tk.Label(self.root, text="No quizzes available for this course.", font=("Arial", 12), bg="#f8c9d8").pack(
                pady=5)

        tk.Button(self.root, text="Back to Courses", command=self.view_courses, bg="#ff0000", fg="white",
                  width=15).pack(pady=10)

    def take_quiz(self, course_id):
        self.clear_screen()

        # استرجاع أسئلة الكويز من قاعدة البيانات
        quizzes = self.db.get_quizzes(course_id)
        print("Fetched quizzes:", quizzes)  # إضافة هذه السطر للتحقق من الأسئلة

        tk.Label(self.root, text=f"Quiz for Course ID: {course_id}", font=("Arial", 18), bg="#f8c9d8").pack(pady=20)

        if not quizzes:
            tk.Label(self.root, text="No quizzes available for this course.", font=("Arial", 14), bg="#f8c9d8").pack(
                pady=20)
            return

        self.quiz_answers = {}
        for idx, (quiz_id, question) in enumerate(quizzes, 1):
            tk.Label(self.root, text=f"{idx}. {question}", bg="#f8c9d8").pack()
            answer_var = tk.StringVar()
            tk.Entry(self.root, textvariable=answer_var).pack(pady=5)
            self.quiz_answers[question] = (quiz_id, answer_var)

        tk.Button(self.root, text="Submit Quiz", command=lambda: self.submit_quiz(course_id), bg="#ff0000", fg="white",
                  width=20).pack(pady=10)
        tk.Button(self.root, text="Back to Course", command=lambda: self.view_course_details(course_id), bg="#ff0000",
                  fg="white", width=15).pack(pady=5)

    def submit_quiz(self, course_id):
        score = 0
        for question, (quiz_id, answer_var) in self.quiz_answers.items():
            student_answer = answer_var.get().strip()
            if student_answer:
                # إرسال الإجابة إلى قاعدة البيانات
                student_id = 1  # افتراضياً، يجب أن يتم تمرير معرف الطالب الفعلي
                self.db.submit_answer(quiz_id, student_id, student_answer)

                # استرجاع الإجابة الصحيحة من قاعدة البيانات
                correct_answer = self.db.get_correct_answer(quiz_id)
                if student_answer.lower() == correct_answer.lower():
                    score += 1

        messagebox.showinfo("Quiz Submitted", f"Your score: {score}/{len(self.quiz_answers)}")
        self.view_course_details(course_id)

    def view_video(self, video_link):
        if video_link:
            webbrowser.open(video_link)  # فتح الرابط في المتصفح الافتراضي

    def view_pdf(self, pdf_link):
        if pdf_link:
            webbrowser.open(pdf_link)  # فتح الرابط في المتصفح الافتراضي


    def contact_instructor(self):
        self.clear_screen()
        tk.Label(self.root, text="👨‍🏫 Contact Instructor 👨‍🏫", font=("Comic Sans MS", 20, "bold"),
                 bg="#f8c9d8").pack(pady=20)

        tk.Label(self.root, text="Message:", font=("Arial", 15, "bold"), bg="#f8c9d8").pack(
            pady=20)
        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack(pady=5)

        tk.Button(self.root, text="Send Message", command=self.send_message, bg="#ff0000", fg="white", width=15).pack(
            pady=10)
        tk.Button(self.root, text="View Responses", command=self.view_responses, bg="#2196f3", fg="white",
                  width=15).pack(pady=5)

        tk.Button(self.root, text="Back to Main Menu", command=self.main_menu, bg="#ff0000", fg="white", width=15).pack(
            pady=5)

    def send_message(self):
        message = self.message_entry.get()
        if message:

            database_query.add_query(self.student_details[1], message)
            messagebox.showinfo("Success", "Your message has been sent!")
            self.message_entry.delete(0, tk.END)  # تفريغ حقل الإدخال
        else:
            messagebox.showerror("Error", "Please enter a message before sending.")

    def view_responses(self):
        responses_window = tk.Toplevel(self.root)
        responses_window.title("Your Questions and Responses")
        responses_window.geometry("500x300")
        responses_window.configure(bg="#f0f0f0")

        responses = database_query.get_answered_queries(self.logged_in_user['name'])

        if not responses:
            tk.Label(responses_window, text="No responses yet.", bg="#f0f0f0", font=("Arial", 12)).pack(pady=20)
        else:
            for query, response in responses:
                frame = tk.Frame(responses_window, bg="#ffffff", bd=1, relief="solid")
                frame.pack(pady=5, padx=10, fill="x")
                tk.Label(frame, text=f"Q: {query}", bg="#ffffff", font=("Arial", 10, "bold")).pack(anchor="w", padx=5)
                tk.Label(frame, text=f"A: {response}", bg="#ffffff", font=("Arial", 10)).pack(anchor="w", padx=5)

    def logout(self):
        self.logged_in_user = None
        self.login_screen()

    def clear_screen(self):

        for widget in self.root.winfo_children():
            widget.destroy()


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = EducationalPlatform(root)
    root.mainloop()
