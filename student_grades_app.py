"""  Date: 5th May 2021
     Code by: Viyeta Kansara
     CWID: 10473081

     About Development: Displaying Student Grade table from Python with Flask using base.html and student_course.html

"""

from flask import Flask, render_template
from typing import Dict, List
import sqlite3

DB_FILE: str = "student_repo.sqlite"

app: Flask = Flask(__name__)


@app.route("/student_grades")
def student_grades_table_db():
    """Using 'db_path' by specifying the path of SQLite database file. Executing the student
    grades summary query using Python calls and then executing the query"""

    db: sqlite3.Connection = sqlite3.connect(DB_FILE)
    query: str = """SELECT s.Name, s.CWID,g.Course, g.grade, i.Name FROM students s JOIN grades g 
                     ON s.CWID = g.StudentCWID JOIN instructors i ON g.InstructorCWID = i.CWID
                     ORDER BY s.Name"""
    data: List[Dict[str, str]] = [
        {
            "name": name,
            "cwid": cwid,
            "course": course,
            "grade": grade,
            "instructor": instructor,
        }
        for name, cwid, course, grade, instructor in db.execute(query)
    ]

    db.close()

    return render_template(
        "student_course.html",
        title="Stevens Repository",
        table_title="Student, Course, Grade, and Instructor",
        students=data,
    )


app.run(debug=True)
