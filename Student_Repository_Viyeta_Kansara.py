"""  Date: 27th April 2021
     Code by: Viyeta Kansara
     CWID: 10473081

     About Development: Assignment is to do following task:
                        1) Update your code to use the new data files that use '\t' to separate the fields and each file
                        has a header record
                        2) Add a new student_grades_table_db(self, db_path) method to your Repository class to create a
                        new student grades PrettyTable that retrieves the data for the table from the database you
                        created above using 'db_path' to specify the path of your SQLite database file.

"""

from prettytable import PrettyTable
from collections import defaultdict
from functools import reduce
import os
import sqlite3


class Repository:
    """Repository class is used to read data files, Check files, and holds all of the data for a specific
    organization"""

    def __init__(self, directory: str) -> None:
        """Check path for directory"""
        self.directory: str = directory

        # Here key is major as it's unique id
        self.major_dict = {}
        # Here Key is student cwid value as it's unique id
        self.student_dict = {}
        # Here Key is Instructor cwid value as it's unique id
        self.instructor_dict = {}
        # Here Key is Grade value as it's unique id
        self.grade_to_number_dict = {}

        self.db_path = "student_repo.sqlite"

        self.major(os.path.join(self.directory, "majors.txt"))
        self.student(os.path.join(self.directory, "students.txt"))
        self.instructor(os.path.join(self.directory, "instructors.txt"))
        self.grades_to_numbers(os.path.join(self.directory, "grades_to_numbers.txt"))
        self.process_grades(os.path.join(self.directory, "grades.txt"))

        print(f"\nDirectory: {self.directory}")
        print("Majors Summary")
        self.pretty_table_major()
        print("Student Summary")
        self.pretty_table_student()
        print("Instructor Summary")
        self.pretty_table_instructor()
        print("Student Grade Summary")
        self.pretty_table_student_grades_table_db()

    def major(self, path):
        """Check for valid major file and create major dictionary"""
        try:
            major_file = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError(
                "Error occurred while opening the major file in this directory"
            )
        else:
            if major_file.readlines() == ["\n"]:
                print("This file is an empty!")
            else:
                major_file.seek(0)
                major_file.readline()
                for lines in major_file:
                    if len(lines.strip().split("\t")) != 3:
                        raise IndexError("Line doesn't have 3 fields")
                    major, flag, course = lines.strip().split("\t")
                    if major not in self.major_dict:
                        self.major_dict[major] = {}

                    if flag not in self.major_dict[major]:
                        self.major_dict[major][flag] = []

                    self.major_dict[major][flag].append(course)
                major_file.close()

    def student(self, path):
        """Check for valid student file and create student dictionary"""
        try:
            student_file = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError(
                "Error occurred while opening the student file in this directory"
            )
        else:
            if student_file.readlines() == ["\n"]:
                print("This file is an empty!")
            else:
                student_file.seek(0)
                student_file.readline()
                for lines in student_file:
                    if len(lines.strip().split("\t")) != 3:
                        raise IndexError("Line doesn't have 3 fields")
                    student_id, student_name, student_major = lines.strip().split("\t")
                    self.student_dict[student_id] = Student(
                        student_id, student_name, student_major
                    )
                student_file.close()

    def instructor(self, path):
        """Check for valid instructor file and create instructor dictionary"""
        try:
            instructor_file = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError("Error occurred while opening the file to analyze")
        else:
            if instructor_file.readlines() == ["\n"]:
                print("This file is an empty!")
            else:
                instructor_file.seek(0)
                instructor_file.readline()
                for lines in instructor_file:
                    if len(lines.strip().split("\t")) != 3:
                        raise IndexError("Line doesn't have 3 fields")
                    (
                        instructor_id,
                        instructor_name,
                        instructor_dept,
                    ) = lines.strip().split("\t")
                    self.instructor_dict[instructor_id] = Instructor(
                        instructor_id, instructor_name, instructor_dept
                    )
                instructor_file.close()

    def grades_to_numbers(self, path):
        """Check for valid grades_to_numbers file and create grades_to_numbers dictionary"""
        try:
            grades_to_numbers_file = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError("Error occurred while opening the file to analyze")
        else:
            if grades_to_numbers_file.readlines() == ["\n"]:
                print("This file is an empty!")
            else:
                grades_to_numbers_file.seek(0)
                for lines in grades_to_numbers_file:
                    if len(lines.strip().split("\t")) != 2:
                        raise IndexError("Line doesn't have 2 fields")
                    (grade, number) = lines.strip().split("\t")
                    self.grade_to_number_dict[grade] = float(number)
                grades_to_numbers_file.close()

    def process_grades(self, path):
        """Check for valid grades file, and create course grade dictionary for students info"""
        try:
            grade_file = open(path, "r")
        except FileNotFoundError:
            raise FileNotFoundError(
                "There is an error with opening the file to analyze"
            )
        else:
            if grade_file.readlines() == ["\n"]:
                print("This file is an empty.")
            else:
                grade_file.seek(0)
                grade_file.readline()
                for lines in grade_file:
                    if len(lines.strip().split("\t")) != 4:
                        raise IndexError("Line doesn't have 4 fields")
                    (
                        student_id,
                        student_course,
                        student_grade,
                        instructor_id,
                    ) = lines.strip().split("\t")
                    if student_id in self.student_dict:
                        s = self.student_dict[student_id]
                        s.add_course_grade(student_course, student_grade)
                    else:
                        print("Unknown student found")

                    if instructor_id in self.instructor_dict:
                        self.instructor_dict[instructor_id].add_course_student(
                            student_course
                        )
                    else:
                        print("Unknown Instructor found")

                grade_file.close()

    def student_grades_table_db(self, db_path="student_repo.sqlite"):
        """Using 'db_path' by specifying the path of SQLite database file. Executing the student
        grades summary query using Python calls and then executing the query to generate and display a
        student grades PrettyTable with the results."""

        self.db_path = db_path
        db: sqlite3.Connection = sqlite3.connect(self.db_path)
        query: str = """SELECT s.Name, s.CWID,g.Course, g.grade, i.Name FROM students s JOIN grades g 
                         ON s.CWID = g.StudentCWID JOIN instructors i ON g.InstructorCWID = i.CWID
                         ORDER BY s.Name"""
        for row in db.execute(query):
            # [Student Name, Student CWID, Course, Grade, Instructor Name]
            yield [row[0], row[1], row[2], row[3], row[4]]

    def pretty_table_student_grades_table_db(self):
        """Print all student grade info pretty table"""
        pt = PrettyTable(field_names=["Name", "CWID", "Course", "Grade", "Instructor"])
        for m in self.student_grades_table_db():
            pt.add_row(m)
        print(pt)

    def pretty_table_major(self):
        """Print all majors info pretty table"""
        pt = PrettyTable(field_names=["Major", "Required Courses", "Electives"])
        for m in self.major_dict.keys():
            pt.add_row([m, self.major_dict[m]["R"], self.major_dict[m]["E"]])
        print(pt)

    def pretty_table_student(self):
        """Print all students info pretty table"""
        pt = PrettyTable(
            field_names=[
                "CWID",
                "Name",
                "Completed Courses",
                "Remaining Required",
                "Remaining Electives",
                "GPA",
            ]
        )
        for s in self.student_dict.values():
            pt.add_row(
                s.student_details(
                    self.grade_to_number_dict,
                    self.major_dict[s.student_major]["R"],
                    self.major_dict[s.student_major]["E"],
                )
            )
        print(pt)

    def pretty_table_instructor(self):
        """Print all instructors pretty table"""
        pt = PrettyTable(field_names=["CWID", "Name", "Dept", "Course", "Students"])
        for i in self.instructor_dict.values():
            for line in i.instructor_details():
                pt.add_row(line)
        print(pt)


class Student:
    """Student class for creating an instance of one student, and printing individual details"""

    def __init__(self, student_id, student_name, student_major):
        """initializes the name, id number and major; sets list of grades to []"""
        self.student_id = student_id
        self.student_name = student_name
        self.student_major = student_major
        self.course_grades = {}

    def add_course_grade(self, course, grade):
        """Container for course and grade"""
        self.course_grades[course] = grade

    def student_details(
        self, grade_to_number_dict, required_course_list, elective_course_list
    ):
        """Returns the summary data about a single student needed"""
        self.calculate_gpa(grade_to_number_dict)
        self.check_remaining_required_courses(
            required_course_list, grade_to_number_dict
        )
        self.check_remaining_elective_courses(
            elective_course_list, grade_to_number_dict
        )
        return [
            self.student_id,
            self.student_name,
            self.completed_courses(grade_to_number_dict),
            self.remaining_required_courses,
            self.remaining_electives,
            self.gpa,
        ]

    def calculate_gpa(self, grade_to_number_dict):
        """Calculate gpa"""
        numbers_list = [
            grade_to_number_dict[grade] for grade in self.course_grades.values()
        ]
        self.gpa = round(
            reduce(lambda a, b: a + b, numbers_list) / len(self.course_grades.values()),
            2,
        )

    def check_remaining_required_courses(
        self, required_course_list, grade_to_number_dict
    ):
        """Set Remaining Required Courses"""
        completed_course_list = self.completed_courses(grade_to_number_dict)

        self.remaining_required_courses = []

        for e in required_course_list:
            if e not in completed_course_list:
                self.remaining_required_courses.append(e)

        self.remaining_required_courses = sorted(self.remaining_required_courses)

    def check_remaining_elective_courses(
        self, elective_course_list, grade_to_number_dict
    ):
        """Set Remaining Elective Courses"""
        completed_course_list = self.completed_courses(grade_to_number_dict)
        one_elective_passed = False
        for e in elective_course_list:
            if e in completed_course_list:
                one_elective_passed = True

        """Check if student has passed atleast one elective"""
        if one_elective_passed:
            self.remaining_electives = []
        else:
            self.remaining_electives = elective_course_list

    def completed_courses(self, grade_to_number_dict):
        """Get completed courses"""
        return sorted(
            [
                c
                for c in self.course_grades.keys()
                if grade_to_number_dict[self.course_grades[c]] > 0
            ]
        )


class Instructor:
    """Instructor class for creating an instance of one instructor, and printing individual details"""

    def __init__(self, instructor_id, instructor_name, instructor_dept):
        """initializes the name, id number and Department; sets list of number of students to []"""
        self.instructor_id = instructor_id
        self.instructor_name = instructor_name
        self.instructor_dept = instructor_dept
        self.course_students = defaultdict(int)

    def add_course_student(self, course):
        """specify a course, and updates the container of courses taught to increment the number of students by 1"""
        self.course_students[course] += 1

    def instructor_details(self):
        """ Returns information needed by the Instructor """
        for course, student_num in self.course_students.items():
            yield [
                self.instructor_id,
                self.instructor_name,
                self.instructor_dept,
                course,
                student_num,
            ]

    def one_instructor_details(self):
        """ return one line at a time with id, name, course, number of students """
        for course, student_num in self.course_students.items():
            return [
                self.instructor_id,
                self.instructor_name,
                self.instructor_dept,
                course,
                student_num,
            ]


def main():
    """main() function to assign directory for files, and to print prettytables"""
    stevens = Repository(".\\stevens")


if __name__ == "__main__":
    main()
