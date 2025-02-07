import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import re
import sqlite3
import database_query
import class_student
import ins
import webbrowser
from courses_database import CoursesDatabase
db = CoursesDatabase()

def is_valid_url(url):
    pattern = re.compile(r'^(https?://)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}(/.*)?$')
    return bool(pattern.match(url))

database_query.create_table()
ins.create_table()


class InstructorApp:

    def __init__(self, root):
        self.root = root
        self.db = CoursesDatabase()
        self.root.configure(bg="#f0f0f0")


        self.instructor_data = {
            "name": "Sarah Zahran",
            "email": "sarazahran@example.com",
            "password": "S123",
            "phone": "01234567890",
            "courses": [],
            "total_students": 0,
            "students": []
        }

        self.student=class_student.EducationalPlatform(self.root)

        self.show_home_page()




    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def fetch_students_from_db(self):
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name, email, phone_number FROM students")
        students = cursor.fetchall()
        conn.close()
        return students

    def show_student_details(self):
        self.clear_frame()


        canvas = tk.Canvas(self.root, bg="#f0f8ff")
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)


        details_frame = tk.Frame(canvas, bg="#f0f8ff", padx=20, pady=20)


        students = self.fetch_students_from_db()

        if not students:
            tk.Label(details_frame, text="No students registered yet.", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(
                pady=20, anchor="center")
        else:
            tk.Label(details_frame, text=f"Total Students: {len(students)}", font=("Arial", 16, "bold"),
                     bg="#f0f8ff").pack(pady=20, anchor="center")


            for student in students:

                tk.Label(details_frame, text=f"Name: {student[0]}", font=("Arial", 14), bg="#f0f8ff", width=30,
                         anchor="center").pack(pady=5)
                tk.Label(details_frame, text=f"Email: {student[1]}", font=("Arial", 14), bg="#f0f8ff", width=30,
                         anchor="center").pack(pady=5)
                tk.Label(details_frame, text=f"Phone Number: {student[2]}", font=("Arial", 14), bg="#f0f8ff", width=30,
                         anchor="center").pack(pady=5)


                tk.Label(details_frame, text="-" * 50, font=("Arial", 10), bg="#f0f8ff").pack(pady=5)


            button = tk.Button(details_frame, text="Back to Home", command=self.show_home_page, bg="#ff7f50",
                               fg="white",
                               font=("Arial", 14, "bold"))
            button.pack(pady=20)


        canvas.create_window((0, 0), window=details_frame, anchor="nw")
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)


        details_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


        canvas.pack(fill="both", expand=True)

    def show_home_page(self):
        self.clear_frame()

        self.buttons_section()

    def show_instructor_info(self):
        self.clear_frame()
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(self.root, text="👨‍🏫 Instructor Information 👨‍🏫", font=("Comic Sans MS", 20, "bold"), bg="#f8c9d8").pack(
            pady=20)
        infoo= ins.get_instructor_data()


        tk.Label(self.root, text=f"Name : {infoo[0]}" ,font=("Arial", 15, "bold"), bg="#f8c9d8").pack(
            pady=20)
        tk.Label(self.root, text=f"Email : {infoo[1]}", font=("Arial", 15 ,"bold"), bg="#f8c9d8").pack(
            pady=20)
        tk.Label(self.root, text=f"Phone : {infoo[2]}", font=("Arial", 15, "bold"), bg="#f8c9d8").pack(
            pady=20)
        tk.Label(self.root, text=f"Password : {infoo[3]}", font=("Arial", 15, "bold"), bg="#f8c9d8").pack(
            pady=20)

        tk.Button(self.root, text="Update Information", command=self.show_update_info_window, bg="#4CAF50", fg="white",
                  font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(self.root, text="Back to Home", command=self.show_home_page, bg="#ff7f50", fg="white",
                  font=("Arial", 14, "bold")).pack(pady=10)
        tk.Button(self.root, text="Exit ✌", command=self.root.quit, bg="#ff6666", fg="white",
                  font=("Arial", 14, "bold")).pack(pady=10)

    def show_update_info_window(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Information")
        update_window.geometry("400x600")
        update_window.configure(bg="#f0f8ff")

        tk.Label(update_window, text="Update Your Information", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=10)


        ans = ins.get_instructor_data()


        name_entry = self.create_entry(update_window, "Name:", ans[0])
        email_entry = self.create_entry(update_window, "Email:", ans[1])
        password_entry = self.create_entry(update_window, "Password:", ans[3], show="*")
        phone_entry = self.create_entry(update_window, "Phone:", ans[2])

        def validate_and_update():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            phone = phone_entry.get()


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


            ins.update_instructor_info( name, email, phone, password)


            messagebox.showinfo("Success", "Information updated successfully!")
            update_window.destroy()


            self.show_instructor_info()

        tk.Button(update_window, text="Save Changes", command=validate_and_update, bg="#4CAF50", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=20)
        tk.Button(update_window, text="Cancel", command=update_window.destroy, bg="#f44336", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=5)

    def create_entry(self, parent, label_text, default_value, show=None):
        tk.Label(parent, text=label_text, font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        entry = tk.Entry(parent, width=30, show=show)
        entry.insert(0, default_value)
        entry.pack(pady=5)
        return entry


    def buttons_section(self):

        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.place(relx=0.5, rely=0.5, anchor="center")
        button_style = {"font": ("Comic Sans MS", 12, "bold"), "width": 40, "bg": "#ECF0F1", "fg": "blue"}
        tk.Label(self.root, text="☸ Home Page ☸", font=("Comic Sans MS", 20, "bold"), bg="#f8c9d8").pack(
            pady=20)


        tk.Button(buttons_frame, text="My Profile", **button_style, command=self.show_instructor_info).pack(pady=10)
        tk.Button(buttons_frame, text="My Courses", **button_style, command=self.show_my_courses).pack(pady=10)
        tk.Button(buttons_frame, text="Student Details", **button_style, command=self.show_student_details).pack( pady=10)
        tk.Button(buttons_frame, text="Respond to Students' Questions", **button_style,command=self.respond_to_students).pack(pady=20)

        tk.Button(buttons_frame, text="Back to Role section", **button_style, command=self.student_dashboard).pack( pady=10)

    def student_dashboard(self):

        self.student.role_selection_screen()

    def add_course(self):
        add_course_window = tk.Toplevel(self.root)
        add_course_window.title("Add New Course")
        add_course_window.geometry("400x600")
        add_course_window.configure(bg="#f0f8ff")

        tk.Label(add_course_window, text="Add New Course", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)


        tk.Label(add_course_window, text="Course Name:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        course_name_entry = tk.Entry(add_course_window, width=30)
        course_name_entry.pack(pady=5)


        tk.Label(add_course_window, text="Video Link:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        video_link_entry = tk.Entry(add_course_window, width=30)
        video_link_entry.pack(pady=5)


        tk.Label(add_course_window, text="PDF Link:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        pdf_link_entry = tk.Entry(add_course_window, width=30)
        pdf_link_entry.pack(pady=5)

        def validate_and_add_course():
            course_name = course_name_entry.get()
            video_link = video_link_entry.get()
            pdf_link = pdf_link_entry.get()

            if not course_name or not video_link or not pdf_link:
                messagebox.showerror("Error", "Course Name, Video Link, and PDF Link are required!")
                return
            if not is_valid_url(video_link):
                messagebox.showerror("Error", "Invalid video link!")
                return
            if not is_valid_url(pdf_link):
                messagebox.showerror("Error", "Invalid PDF link!")
                return

            try:

                course_id = self.db.add_course(course_name, video_link, pdf_link)

                messagebox.showinfo("Success", "Course added successfully!")


                add_course_window.destroy()
                self.show_my_courses()


                self.add_quiz_window(course_id)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add course: {e}")


                def open_add_quiz_window():
                    self.add_quiz_window(course_id)


                tk.Button(add_course_window, text="Add Quiz", font=("Arial", 12), command=open_add_quiz_window).pack(
                    pady=20)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add course: {e}")


        tk.Button(add_course_window, text="Add Course", font=("Arial", 12), command=validate_and_add_course).pack(
            pady=20)


    def add_quiz_window(self, course_id):
        add_quiz_window = tk.Toplevel(self.root)
        add_quiz_window.title("Add Quiz")
        add_quiz_window.geometry("400x400")
        add_quiz_window.configure(bg="#f0f8ff")

        tk.Label(add_quiz_window, text="Add Quiz", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)

        tk.Label(add_quiz_window, text="Question:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        question_entry = tk.Entry(add_quiz_window, width=30)
        question_entry.pack(pady=5)

        tk.Label(add_quiz_window, text="Correct Answer:", font=("Arial", 12), bg="#f0f8ff").pack(pady=5)
        correct_answer_entry = tk.Entry(add_quiz_window, width=30)
        correct_answer_entry.pack(pady=5)


        def validate_and_add_quiz():
            question = question_entry.get()
            correct_answer = correct_answer_entry.get()

            if not question or not correct_answer:
                messagebox.showerror("Error", "Both question and correct answer are required!")
                return

            try:

                self.db.add_quiz(course_id, question, correct_answer)
                messagebox.showinfo("Success", "Quiz added successfully!")
                add_quiz_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add quiz: {e}")

        tk.Button(add_quiz_window, text="Add Quiz", font=("Arial", 12), command=validate_and_add_quiz).pack(pady=20)

    def submit_answer(self, quiz_id, student_id, student_answer):
        try:
            self.db.submit_answer(quiz_id, student_id, student_answer)
            messagebox.showinfo("Success", "Your answer has been submitted!")
            self.show_my_courses()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit answer: {e}")

    def view_quiz_results(self, course_id):
        quizzes = self.db.get_quizzes(course_id)
        if not quizzes:
            messagebox.showerror("Error", "No quizzes available for this course!")
            return

        quiz_results_window = tk.Toplevel(self.root)
        quiz_results_window.title("Quiz Results")
        quiz_results_window.geometry("400x400")
        quiz_results_window.configure(bg="#f0f8ff")

        tk.Label(quiz_results_window, text="Quiz Results", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)

        for quiz in quizzes:
            quiz_id, question = quiz


            self.db.cursor.execute('''SELECT student_answer, is_answer_correct FROM quizzes WHERE id = ?''',
                                   (quiz_id,))
            result = self.db.cursor.fetchone()
            student_answer, is_answer_correct = result[0], result[1]

            tk.Label(quiz_results_window, text=f"Question: {question}", font=("Arial", 12), bg="#f0f8ff").pack(
                pady=5)
            tk.Label(quiz_results_window, text=f"Your Answer: {student_answer}", font=("Arial", 12),
                     bg="#f0f8ff").pack(
                pady=5)


            if is_answer_correct == 1:
                tk.Label(quiz_results_window, text="Correct", font=("Arial", 12, "bold"), fg="green",
                         bg="#f0f8ff").pack(pady=5)
            else:
                tk.Label(quiz_results_window, text="Incorrect", font=("Arial", 12, "bold"), fg="red",
                         bg="#f0f8ff").pack(pady=5)

    def show_my_courses(self):
        self.clear_frame()


        tk.Label(self.root, text="📚 My Courses 📚", font=("Arial", 20), bg="#f0f8ff", fg="#003366").pack(pady=20)

        try:
            courses = db.get_courses()
            if not courses:
                tk.Label(self.root, text="No courses available.", font=("Arial", 14), bg="#f0f8ff", fg="red").pack(
                    pady=10)
            else:
                for course in courses:
                    course_id, course_name, video_link, pdf_link = course


                    course_frame = tk.Frame(self.root, bg="#f0f8ff", padx=10, pady=10)
                    course_frame.pack(fill="x", padx=20, pady=5)


                    tk.Label(course_frame, text=course_name, font=("Arial", 14, "bold"), bg="#f0f8ff").pack(side="left",
                                                                                                            padx=10)


                    tk.Button(course_frame, text="Edit", command=lambda c_id=course_id: self.edit_course(c_id)).pack(
                        side="left", padx=10)
                    tk.Button(course_frame, text="Delete",
                              command=lambda c_id=course_id: self.delete_courses(c_id)).pack(side="left", padx=10)
                    tk.Button(course_frame, text="View Course", command=lambda c_id=course_id: self.view_course(c_id),
                              bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)


                    tk.Button(course_frame, text="View Quizzes", command=lambda c_id=course_id: self.show_quizzes(c_id),
                              bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)

        except Exception as e:
            tk.Label(self.root, text=f"Error loading courses: {e}", font=("Arial", 14), bg="#f0f8ff", fg="red").pack(
                pady=10)


        tk.Button(self.root, text="Back to Home", command=self.show_home_page, bg="#ff7f50", fg="white",
                  font=("Arial", 14, "bold")).pack(pady=20)


        tk.Button(self.root, text="Add New Course", command=self.add_course, bg="#4CAF50", fg="white",
                  font=("Arial", 14, "bold")).pack(pady=10)
    def edit_course(self, course_id):
        course = db.get_course_by_id(course_id)

        if not course:
            messagebox.showerror("Error", "Course not found!")
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Course")
        edit_window.geometry("400x400")
        edit_window.configure(bg="#f0f8ff")

        tk.Label(edit_window, text="Edit Course Details", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)


        tk.Label(edit_window, text="Course Name:", font=("Arial", 14), bg="#f0f8ff").pack(pady=5)
        course_name_entry = tk.Entry(edit_window, width=30)
        course_name_entry.insert(0, course[1])  # اسم الكورس
        course_name_entry.pack(pady=5)


        tk.Label(edit_window, text="Video Link:", font=("Arial", 14), bg="#f0f8ff").pack(pady=5)
        video_link_entry = tk.Entry(edit_window, width=30)
        video_link_entry.insert(0, course[2])  # رابط الفيديو
        video_link_entry.pack(pady=5)

        # حقل PDF (اختياري)
        tk.Label(edit_window, text="PDF Link (Optional):", font=("Arial", 14), bg="#f0f8ff").pack(pady=5)
        course_pdf_entry = tk.Entry(edit_window, width=30)
        course_pdf_entry.insert(0, course[3] if course[3] else "")  # PDF
        course_pdf_entry.pack(pady=5)

        def update_course():
            course_name = course_name_entry.get()
            video_link = video_link_entry.get()
            course_pdf = course_pdf_entry.get() if course_pdf_entry.get() else None
            if not is_valid_url(video_link):
                messagebox.showerror("Error", "Invalid video link!")
                return

            try:
                db.update_course(course_id, course_name, video_link, course_pdf)
                messagebox.showinfo("Success", "Course updated successfully!")
                edit_window.destroy()
                self.show_my_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update course: {e}")

        tk.Button(edit_window, text="Update Course", command=update_course, bg="#4CAF50", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=20)


        tk.Button(edit_window, text="Cancel", command=edit_window.destroy, bg="#f44336", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=5)


    def delete_courses(self, course_id):
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this course?")
        if confirm:
            try:
                db.delete_course(course_id)
                messagebox.showinfo("Success", "Course deleted successfully!")
                self.show_my_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete course: {e}")

    def view_course(self, course_id):
        course = db.get_course_by_id(course_id)
        if not course:
            messagebox.showerror("Error", "Course not found!")
            return

        if isinstance(course, tuple):
            view_window = tk.Toplevel(self.root)
            view_window.title("View Course Details")
            view_window.geometry("400x600")
            view_window.configure(bg="#f0f8ff")

            tk.Label(view_window, text="Course Details", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)

            tk.Label(view_window, text=f"Course Name: {course[1]}", font=("Arial", 12, "bold"), bg="#f0f8ff").pack(
                pady=10)

            if course[2]:
                tk.Button(view_window, text="Open Video Link", command=lambda: webbrowser.open(course[2]), bg="#4CAF50",
                          fg="white", font=("Arial", 12, "bold")).pack(pady=10)

            if course[3]:
                tk.Button(view_window, text="Open PDF Link", command=lambda: webbrowser.open(course[3]), bg="#4CAF50",
                          fg="white", font=("Arial", 12, "bold")).pack(pady=10)



            tk.Button(view_window, text="Close", command=view_window.destroy, bg="#ff4d4d", fg="white",
                      font=("Arial", 12, "bold")).pack(pady=20)

    def show_quizzes(self, course_id):
        quizzes = db.get_quizzes(course_id)
        if not quizzes:
            messagebox.showinfo("Info", "No quizzes available for this course.")
            return

        quizzes_window = tk.Toplevel(self.root)
        quizzes_window.title("Quizzes")
        quizzes_window.geometry("400x400")
        quizzes_window.configure(bg="#f0f8ff")

        tk.Label(quizzes_window, text="Quiz Questions", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)

        for quiz in quizzes:
            quiz_id, question = quiz

            frame = tk.Frame(quizzes_window, bg="#e6f7ff", padx=10, pady=10, relief="solid", bd=2)
            frame.pack(pady=10, padx=20, fill="x")

            tk.Label(frame, text=f"Question: {question}", font=("Arial", 12), bg="#e6f7ff").pack(anchor="w", pady=5)


            correct_answer = db.get_correct_answer(quiz_id)

            tk.Label(frame, text=f"Correct Answer: {correct_answer}", font=("Arial", 12, "bold"), bg="#e6f7ff",
                     fg="green").pack(anchor="w", pady=5)

        tk.Button(quizzes_window, text="Close", command=quizzes_window.destroy, bg="red", fg="white",
                  font=("Arial", 12, "bold")).pack(pady=20)





    def respond_to_students(self):

        queries_window = tk.Toplevel()
        queries_window.title("Student Queries")
        queries_window.geometry("500x400")
        queries_window.configure(bg="#ECF0F1")




        queries = database_query.get_unanswered_queries()


        for query in queries:
            query_frame = tk.Frame(queries_window, bg="#ffcccc")
            query_frame.pack(pady=10, padx=20, fill="x")

            student_name, query_text = query[0], query[1]

            tk.Label(query_frame, text=f"Student: {student_name}", font=("Arial", 12, "bold"), bg="#ffcccc",
                     fg="#660000").pack()
            tk.Label(query_frame, text=f"Query: {query_text}", font=("Arial", 10), bg="#ffcccc", fg="#660000").pack()


            response_entry = tk.Entry(query_frame, width=40)
            response_entry.pack(pady=5)


            def respond(query=query, entry=response_entry, frame=query_frame):
                response_text = entry.get()
                if response_text:

                    database_query.update_response(query[1], response_text)
                    messagebox.showinfo("Success", "Response added successfully!")


                    entry.delete(0, tk.END)




                else:
                    messagebox.showerror("Error", "Please enter a response.")


            tk.Button(query_frame, text="Respond", command=respond, bg="#ff3333", fg="white").pack(pady=10)


        tk.Button(queries_window, text="Close", command=queries_window.destroy, bg="#ff3333", fg="white").pack(pady=20)



