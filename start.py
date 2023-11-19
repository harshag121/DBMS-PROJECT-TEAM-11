import streamlit as st
import mysql.connector
from datetime import date

# Connect to the MySQL database
# Replace 'your_database', 'your_username', 'your_password' with actual database credentials
db = mysql.connector.connect(
    host="localhost",
    user="schoolAdmin",
    passwd="hgschool",
    database="schoolDatabase"
)
cursor = db.cursor()

# Function to create a student
def create_student(name, roll_number, age, grade):
    query = "INSERT INTO students (name, roll_number, age, grade) VALUES (%s, %s, %s, %s)"
    values = (name, roll_number, age, grade)
    cursor.execute(query, values)
    db.commit()

# Function to get all students
def get_all_students():
    query = "SELECT * FROM students"
    cursor.execute(query)
    return cursor.fetchall()

# Function to display students in table format
def display_students_table():
    st.header("Student Information")
    students = get_all_students()
    st.table(students)

# Function to delete attendance for a student
def delete_attendance(student_id):
    query = "DELETE FROM attendance WHERE student_id = %s"
    values = (student_id,)
    cursor.execute(query, values)
    db.commit()

# Function to delete a student
def delete_student(student_id):
    # Delete attendance records for the student
    delete_attendance(student_id)

    # Delete the student
    query = "DELETE FROM students WHERE student_id = %s"
    values = (student_id,)
    cursor.execute(query, values)
    db.commit()

# Function to display student information
def display_students():
    st.header("Student Information")
    students = get_all_students()
    for student in students:
        st.write(f"Name: {student[1]}, Roll Number: {student[2]}, Age: {student[3]}, Grade: {student[4]}")

# Function to create a teacher
def create_teacher(name, subject):
    query = "INSERT INTO teachers (name, subject) VALUES (%s, %s)"
    values = (name, subject)
    cursor.execute(query, values)
    db.commit()

# Function to get all teachers
def get_all_teachers():
    query = "SELECT * FROM teachers"
    cursor.execute(query)
    return cursor.fetchall()

# Function to display teachers in table format
def display_teachers_table():
    st.header("Teacher Information")
    teachers = get_all_teachers()
    st.table(teachers)

# Function to delete a teacher
def delete_teacher(teacher_id):
    query = "DELETE FROM teachers WHERE teacher_id = %s"
    values = (teacher_id,)
    cursor.execute(query, values)
    db.commit()

# Function to mark attendance for a student on a given date for a specific course
def mark_attendance(student_id, course_id):
    query = "INSERT INTO attendance (student_id, course_id, date) VALUES (%s, %s, %s)"
    values = (student_id, course_id, date.today())
    cursor.execute(query, values)
    db.commit()

# Function to get attendance for a specific student in a specific course
def get_student_attendance(student_id, course_id):
    query = "SELECT * FROM attendance WHERE student_id = %s AND course_id = %s"
    values = (student_id, course_id)
    cursor.execute(query, values)
    return cursor.fetchall()

# Function to display attendance for a specific student in a specific course
def display_attendance(student_id, course_id):
    st.header("Attendance Records")
    attendance_records = get_student_attendance(student_id, course_id)
    
    if not attendance_records:
        st.warning("No attendance records found for the selected student in the course.")
        return

    for record in attendance_records:
        st.write(f"Date: {record[3]}")

# Function to add a new student
def add_new_student():
    st.subheader("Add New Student")
    name = st.text_input("Name")
    roll_number = st.number_input("Roll Number", step=1, format="%d")
    age = st.number_input("Age", step=1, format="%d")
    grade = st.text_input("Grade")
    
    if st.button("Add Student"):
        create_student(name, roll_number, age, grade)
        st.success("Student added successfully!")

# Function to add a new teacher
def add_new_teacher():
    st.subheader("Add New Teacher")
    name = st.text_input("Name")
    subject = st.text_input("Subject")
    
    if st.button("Add Teacher"):
        create_teacher(name, subject)
        st.success("Teacher added successfully!")

# Function to delete a student
def delete_student_ui():
    st.subheader("Delete Student")
    students = get_all_students()
    student_names = [student[1] for student in students]

    if not student_names:
        st.warning("No students found to delete.")
        return

    selected_student = st.selectbox("Select a student to delete", student_names)
    student_id = next((student[0] for student in students if student[1] == selected_student), None)

    if student_id is not None:
        if st.button("Delete Student"):
            delete_student(student_id)
            st.success(f"Student '{selected_student}' deleted successfully!")
    else:
        st.warning("Selected student not found.")

# Function to delete a teacher
def delete_teacher_ui():
    st.subheader("Delete Teacher")
    teachers = get_all_teachers()
    teacher_names = [teacher[1] for teacher in teachers]
    selected_teacher = st.selectbox("Select a teacher to delete", teacher_names)
    teacher_id = next((teacher[0] for teacher in teachers if teacher[1] == selected_teacher), None)
    
    if teacher_id is not None:
        if st.button("Delete Teacher"):
            delete_teacher(teacher_id)
            st.success(f"Teacher '{selected_teacher}' deleted successfully!")
    else:
        st.warning("Selected teacher not found.")

# Function to add a new course
def add_new_course():
    course_name = st.text_input("Course Name")
    if st.button("Add Course"):
        query = "INSERT INTO courses (course_name) VALUES (%s)"
        values = (course_name,)
        cursor.execute(query, values)
        db.commit()
        st.success(f"Course '{course_name}' added successfully!")

# Function to get all courses
def get_all_courses():
    query = "SELECT * FROM courses"
    cursor.execute(query)
    return cursor.fetchall()

# Function to delete a course
def delete_course(course_id):
    query = "DELETE FROM courses WHERE course_id = %s"
    values = (course_id,)
    cursor.execute(query, values)
    db.commit()

# Function to display courses in table format
def display_courses_table():
    st.header("Course Information")
    courses = get_all_courses()
    st.table(courses)

# Function to delete a course
def delete_course_ui():
    st.subheader("Delete Course")
    courses = get_all_courses()
    course_names = [course[1] for course in courses]

    if not course_names:
        st.warning("No courses found to delete.")
        return

    selected_course = st.selectbox("Select a course to delete", course_names)
    course_id = next((course[0] for course in courses if course[1] == selected_course), None)

    if course_id is not None:
        if st.button("Delete Course"):
            delete_course(course_id)
            st.success(f"Course '{selected_course}' deleted successfully!")
    else:
        st.warning("Selected course not found.")

# Function to mark attendance for a student on a given date for a specific course
def mark_attendance_ui():
    st.subheader("Mark Attendance")
    
    # Get all students
    students = get_all_students()
    student_names = [student[1] for student in students]

    if not student_names:
        st.warning("No students found.")
        return

    # Select a student
    selected_student = st.selectbox("Select a student", student_names)
    student_id = next((student[0] for student in students if student[1] == selected_student), None)

    # Get all courses
    courses = get_all_courses()
    course_names = [course[1] for course in courses]

    if not course_names:
        st.warning("No courses found.")
        return

    # Select a course
    selected_course = st.selectbox("Select a course", course_names)
    course_id = next((course[0] for course in courses if course[1] == selected_course), None)

    # Mark attendance
    if st.button("Mark Attendance"):
        mark_attendance(student_id, course_id)
        st.success(f"Attendance marked for '{selected_student}' in '{selected_course}' on {date.today()}")

# Streamlit UI
def main():
    st.title("School Management System")

    # Sidebar navigation
    menu = ["Home", "Students", "Teachers", "Courses", "Attendance", "Add Student", "Add Teacher", "Add Course", "Delete Student", "Delete Teacher", "Delete Course", "Mark Attendance"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to the School Management System!")
    elif choice == "Students":
        display_students_table()
    elif choice == "Teachers":
        st.subheader("Manage Teachers")
        display_teachers_table()
    elif choice == "Courses":
        st.subheader("Manage Courses")
        display_courses_table()
    elif choice == "Attendance":
        st.subheader("Attendance Management")

        # Get all students and courses
        students = get_all_students()
        courses = get_all_courses()

        # Display a form to select student and course
        selected_student = st.selectbox("Select a student", [student[1] for student in students])
        selected_course = st.selectbox("Select a course", [course[1] for course in courses])

        # Get student_id and course_id
        student_id = next((student[0] for student in students if student[1] == selected_student), None)
        course_id = next((course[0] for course in courses if course[1] == selected_course), None)

        # Display attendance for the selected student and course
        display_attendance(student_id, course_id)

    elif choice == "Add Student":
        add_new_student()
    elif choice == "Add Teacher":
        add_new_teacher()
    elif choice == "Add Course":
        add_new_course()
    elif choice == "Delete Student":
        delete_student_ui()
    elif choice == "Delete Teacher":
        delete_teacher_ui()
    elif choice == "Delete Course":
        delete_course_ui()
    elif choice == "Mark Attendance":
        mark_attendance_ui()

# Run the Streamlit app
if __name__ == "__main__":
    main()
