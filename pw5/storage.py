import os
import pickle
import zlib
import bz2
import lzma
from domains import Student, Course


DATA_FILE = "students.dat"
STUDENTS_FILE = "students.txt"
COURSES_FILE = "courses.txt"
MARKS_FILE = "marks.txt"

COMPRESSION_METHODS = {
    "1": ("zlib", zlib.compress, zlib.decompress),
    "2": ("bz2", bz2.compress, bz2.decompress),
    "3": ("lzma", lzma.compress, lzma.decompress)
}


def save_students(students):
    with open(STUDENTS_FILE, "w") as f:
        for s in students:
            f.write(f"{s.id},{s.name},{s.dob}\n")


def save_courses(courses):
    with open(COURSES_FILE, "w") as f:
        for c in courses:
            f.write(f"{c.id},{c.name},{c.credit}\n")


def save_marks(marks):
    with open(MARKS_FILE, "w") as f:
        for course_id, student_marks in marks.items():
            for student_id, mark in student_marks.items():
                f.write(f"{course_id},{student_id},{mark}\n")


def load_students():
    students = []
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    students.append(Student(parts[0], parts[1], parts[2]))
    return students


def load_courses():
    courses = []
    if os.path.exists(COURSES_FILE):
        with open(COURSES_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    courses.append(Course(parts[0], parts[1], int(parts[2])))
    return courses


def load_marks():
    marks = {}
    if os.path.exists(MARKS_FILE):
        with open(MARKS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    course_id, student_id, mark = parts
                    if course_id not in marks:
                        marks[course_id] = {}
                    marks[course_id][student_id] = float(mark)
    return marks


def compress_data(method_key="1"):
    if method_key not in COMPRESSION_METHODS:
        method_key = "1"

    name, compress_func, _ = COMPRESSION_METHODS[method_key]

    data = {
        "method": method_key,
        "students": open(STUDENTS_FILE, "r").read() if os.path.exists(STUDENTS_FILE) else "",
        "courses": open(COURSES_FILE, "r").read() if os.path.exists(COURSES_FILE) else "",
        "marks": open(MARKS_FILE, "r").read() if os.path.exists(MARKS_FILE) else ""
    }

    pickled = pickle.dumps(data)
    compressed = compress_func(pickled)

    with open(DATA_FILE, "wb") as f:
        f.write(method_key.encode() + b"\n" + compressed)

    for file in [STUDENTS_FILE, COURSES_FILE, MARKS_FILE]:
        if os.path.exists(file):
            os.remove(file)

    return name


def decompress_data():
    if not os.path.exists(DATA_FILE):
        return False

    with open(DATA_FILE, "rb") as f:
        content = f.read()

    method_key = content[:1].decode()
    compressed = content[2:]

    if method_key not in COMPRESSION_METHODS:
        method_key = "1"

    _, _, decompress_func = COMPRESSION_METHODS[method_key]
    data = pickle.loads(decompress_func(compressed))

    if data["students"]:
        with open(STUDENTS_FILE, "w") as f:
            f.write(data["students"])
    if data["courses"]:
        with open(COURSES_FILE, "w") as f:
            f.write(data["courses"])
    if data["marks"]:
        with open(MARKS_FILE, "w") as f:
            f.write(data["marks"])

    os.remove(DATA_FILE)
    return True
