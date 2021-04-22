"""  Date: 21st April 2021
     Code by: Viyeta Kansara
     About Development:Create HW09_Test_Viyeta_Kansara.py file
     which should import class from HW10_Viyeta_Kansara,
     and then define the test cases for each.
"""

import unittest
import os
import Student_Repository_Viyeta_Kansara as hw10


class StudentsTest(unittest.TestCase):
    def test_student_details(self):
        """testing for student_details() method"""
        grade_to_number_dict = {
            "A": 4.0,
            "A-": 3.75,
            "B+": 3.25,
            "B": 3.0,
            "B-": 2.75,
            "C+": 2.25,
            "C": 2.0,
            "C-": 0.0,
            "D+": 0.0,
            "D": 0.0,
            "D-": 0.0,
            "F": 0.0,
        }
        student = hw10.Student("10115", "Wyatt, X", "SFEN")
        student.add_course_grade("SSW 687", "A")
        self.assertEqual(
            student.student_details(grade_to_number_dict, [], []),
            ["10115", "Wyatt, X", ["SSW 687"], [], [], 4.0],
        )
        self.assertNotEqual(
            student.student_details(grade_to_number_dict, [], []),
            ["10172", "Baldwin, C", ["SSW 687"], [], [], 4.0],
        )


class InstructorTest(unittest.TestCase):
    def test_instructor_details(self):
        """testing for instructor_details() method"""
        instructor = hw10.Instructor("98765", "Einstein, A", "SFEN")
        instructor.add_course_student("SSW 567")
        self.assertEqual(
            instructor.one_instructor_details(),
            ["98765", "Einstein, A", "SFEN", "SSW 567", 1],
        )


class RepositoryTest(unittest.TestCase):
    def test_Repository(self):
        """testing for Repository class methods"""
        directory = "D:\\Stevens\\810\\HW10\\stevens"
        repo = hw10.Repository(directory)
        self.assertEqual(repo.student(os.path.join(directory, "students.txt")), None)
        self.assertEqual(
            repo.instructor(os.path.join(directory, "instructors.txt")), None
        )
        self.assertEqual(
            repo.process_grades(os.path.join(directory, "grades.txt")), None
        )
        self.assertEqual(repo.major(os.path.join(directory, "majors.txt")), None)


if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
