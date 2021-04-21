"""  Date: 13th April 2021
     Code by: Viyeta Kansara
     CWID: 10473081

     About Development: Assignment is to create a data repository of courses, students, and instructors.  The system
     will be used to help students track their required courses, the courses they have successfully completed, their
     grades,  GPA, etc.  The system will also be used by faculty advisors to help students to create study plans.
"""

from prettytable import PrettyTable
from collections import defaultdict
import os


class Repository:
    """Repository class is used to read data files, Check files, and holds all of the data for a specific
    organization"""

    def __init__(self, directory: str) -> None:
        """Check path for directory"""
        self.directory: str = directory

        # Here Key is student cwid value as it's unique id
        self.student_dict = {}
        # Here Key is Instructor cwid value as it's unique id
        self.instructor_dict = {}

        self.student(os.path.join(self.directory, "students.txt"))
        self.instructor(os.path.join(self.directory, "instructors.txt"))
        self.process_grades(os.path.join(self.directory, "grades.txt"))

        print(f"\nDirectory: {self.directory}")
        print("Student Summary")
        self.pretty_table_student()
        print("Instructor Summary")
        self.pretty_table_instructor()

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

    def pretty_table_student(self):
        """Print all students info pretty table"""
        pt = PrettyTable(field_names=["CWID", "Name", "Completed Courses"])
        for s in self.student_dict.values():
            pt.add_row(s.student_details())
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

    def student_details(self):
        """Returns the summary data about a single student needed"""
        return [self.student_id, self.student_name, sorted(self.course_grades.keys())]


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
    stevens = Repository("D:\\Stevens\\810\\HW09\\stevens")
    test = Repository("D:\\Stevens\\810\\HW09\\test")
    njit = Repository("D:\\Stevens\\810\\HW09\\njit")


if __name__ == "__main__":
    main()
