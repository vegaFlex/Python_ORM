import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student
from datetime import datetime


def validate_and_convert_date(date_str):
    try:
        # Try to parse the date string in the expected format
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        # Convert the date object to the desired format
        formatted_date = date_obj.strftime('%Y-%m-%d')
        return formatted_date
    except ValueError:
        # Return an error message if the date format is invalid
        return f"Value '{date_str}' has an invalid date format. It must be in YYYY-MM-DD format."


# Creating Records in Database
def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        # birth_date='15-05-1995',
        birth_date=validate_and_convert_date('15-05-1995'),
        email='john.doe@university.com'
    )

    student = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com'
    )
    student.save()

    Student.objects.create(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        # birth_date='10-02-1998',
        birth_date=validate_and_convert_date('10-02-1998'),
        email='alice.johnson@university.com'
    )

    student = Student(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date=validate_and_convert_date('5-11-1996'),
        email='bob.wilson@university.com'
    )
    student.save()


# add_students()
# print(Student.objects.all())


# Reading Data from the Database
def get_students_info():
    result = []
    students = Student.objects.all()
    for student in students:
        result.append(f"Student №{student.student_id}:"
                      f" {student.first_name} {student.last_name};"
                      f" Email: {student.email}")
    return '\n'.join(result)


# Updating a Record in Database
def update_students_emails():
    students = Student.objects.all()
    for student in students:
        student.email = student.email.replace(student.email.split('@')[1], 'uni-students.com')
        student.save()


# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)


# Deleting a Record from Database
def truncate_students():
    Student.objects.all().delete()

# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")
