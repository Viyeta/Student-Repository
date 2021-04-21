"""  Date: 13th April 2021
     Code by: Viyeta Kansara
     About Development:Create Student_Repository_Test_Viyeta_Kansara.py file
     which should import class from Student_Repository_Viyeta_Kansara,
     and then define the test cases for each.
"""

import unittest
import os
import Student_Repository_Viyeta_Kansara as hw9


class StudentsTest(unittest.TestCase):
    def test_student_details(self):
        """testing for student_details() method"""
        student = hw9.Student("10115", "Wyatt, X", "SFEN")
        student.add_course_grade("SSW 687", "A")
        self.assertEqual(student.student_details(), ["10115", "Wyatt, X", ["SSW 687"]])


class InstructorTest(unittest.TestCase):
    def test_instructor_details(self):
        """testing for instructor_details() method"""
        instructor = hw9.Instructor("98765", "Einstein, A", "SFEN")
        instructor.add_course_student("SSW 567")
        self.assertEqual(
            instructor.one_instructor_details(),
            ["98765", "Einstein, A", "SFEN", "SSW 567", 1],
        )


class RepositoryTest(unittest.TestCase):
    def test_Repository(self):
        """testing for Repository class methods"""
        directory = "D:\\Stevens\\810\\HW09\\stevens"
        repo = hw9.Repository(directory)
        self.assertEqual(repo.student(os.path.join(directory, "students.txt")), None)
        self.assertEqual(
            repo.instructor(os.path.join(directory, "instructors.txt")), None
        )
        self.assertEqual(
            repo.process_grades(os.path.join(directory, "grades.txt")), None
        )


if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
