#!/usr/bin/env python3

import curses
import math
import os
import pickle
import zipfile

import numpy as np


class Student:
    def __init__(self, student_id="", name="", dob=""):
        self.__id = student_id
        self.__name = name
        self.__dob = dob
        self.__marks = {}
    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def dob(self):
        return self.__dob
    
    @property
    def marks(self):
        return self.__marks.copy()
    
    def set_mark(self, course_id, mark):
        self.__marks[course_id] = math.floor(mark * 10) / 10
    
    def get_mark(self, course_id):
        return self.__marks.get(course_id)
    
    def input(self):
        self.__id = input("  Student ID: ").strip()
        self.__name = input("  Name: ").strip()
        self.__dob = input("  DoB (DD/MM/YYYY): ").strip()
    
    def __str__(self):
        return f"{self.__id} | {self.__name} | {self.__dob}"


class Course:
    def __init__(self, course_id="", name="", credits=0):
        self.__id = course_id
        self.__name = name
        self.__credits = credits
    
    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def credits(self):
        return self.__credits
    
    def input(self):
        self.__id = input("  Course ID: ").strip()
        self.__name = input("  Name: ").strip()
        while True:
            try:
                self.__credits = int(input("  Credits: "))
                break
            except ValueError:
                print("  Invalid number!")
    
    def __str__(self):
        return f"{self.__id} | {self.__name} | {self.__credits} credits"


def input_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid number!")


def input_students(students):
    n = input_number("Number of students: ")
    for i in range(n):
        print(f"\n--- Student {i+1} ---")
        s = Student()
        s.input()
        students.append(s)
    write_students_txt(students)


def input_courses(courses):
    n = input_number("Number of courses: ")
    for i in range(n):
        print(f"\n--- Course {i+1} ---")
        c = Course()
        c.input()
        courses.append(c)
    write_courses_txt(courses)


def input_marks(students, courses):
    if not courses or not students:
        print("No courses or students!")
        return
    
    print("\n--- Courses ---")
    for i, c in enumerate(courses):
        print(f"  {i+1}. {c}")
    
    choice = input_number("Select course: ") - 1
    if not (0 <= choice < len(courses)):
        print("Invalid!")
        return
    
    course = courses[choice]
    print(f"\nMarks for {course.name}:")
    for s in students:
        while True:
            try:
                mark = float(input(f"  {s.name}: "))
                if 0 <= mark <= 20:
                    s.set_mark(course.id, mark)
                    break
                print("  Mark must be 0-20!")
            except ValueError:
                print("  Invalid!")
    write_marks_txt(students)


def list_students(students):
    print("\n--- Students ---")
    for s in students:
        print(f"  {s}")


def list_courses(courses):
    print("\n--- Courses ---")
    for c in courses:
        print(f"  {c}")


def show_marks(students, courses):
    if not courses:
        print("No courses!")
        return
    
    print("\n--- Courses ---")
    for i, c in enumerate(courses):
        print(f"  {i+1}. {c}")
    
    choice = input_number("Select course: ") - 1
    if not (0 <= choice < len(courses)):
        return
    
    course = courses[choice]
    print(f"\n--- Marks for {course.name} ---")
    for s in students:
        mark = s.get_mark(course.id)
        print(f"  {s.id} | {s.name} | {mark if mark else 'N/A'}")


def calculate_gpa(student, courses):
    marks = []
    credits = []
    for c in courses:
        m = student.get_mark(c.id)
        if m is not None:
            marks.append(m)
            credits.append(c.credits)
    
    if not marks:
        return 0.0
    
    marks_arr = np.array(marks)
    credits_arr = np.array(credits)
    return float(np.sum(marks_arr * credits_arr) / np.sum(credits_arr))


def sort_by_gpa(students, courses):
    gpa_list = [(s, calculate_gpa(s, courses)) for s in students]
    gpa_list.sort(key=lambda x: x[1], reverse=True)
    
    students.clear()
    students.extend([x[0] for x in gpa_list])
    
    print("\n--- Students by GPA ---")
    for s, gpa in gpa_list:
        print(f"  {s.id} | {s.name} | GPA: {gpa:.2f}")


def write_students_txt(students):
    with open("students.txt", "w") as f:
        for s in students:
            f.write(f"{s.id},{s.name},{s.dob}\n")
    print("Saved students.txt")


def write_courses_txt(courses):
    with open("courses.txt", "w") as f:
        for c in courses:
            f.write(f"{c.id},{c.name},{c.credits}\n")
    print("Saved courses.txt")


def write_marks_txt(students):
    with open("marks.txt", "w") as f:
        for s in students:
            for cid, mark in s.marks.items():
                f.write(f"{s.id},{cid},{mark}\n")
    print("Saved marks.txt")


def load_students_txt():
    students = []
    if os.path.exists("students.txt"):
        with open("students.txt") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    students.append(Student(parts[0], parts[1], parts[2]))
    return students


def load_courses_txt():
    courses = []
    if os.path.exists("courses.txt"):
        with open("courses.txt") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    courses.append(Course(parts[0], parts[1], int(parts[2])))
    return courses


def load_marks_txt(students):
    if os.path.exists("marks.txt"):
        with open("marks.txt") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    sid, cid, mark = parts[0], parts[1], float(parts[2])
                    for s in students:
                        if s.id == sid:
                            s.set_mark(cid, mark)
                            break


DATA_FILE = "students.dat"


def compress_to_dat():
    files = ["students.txt", "courses.txt", "marks.txt"]
    existing = [f for f in files if os.path.exists(f)]
    
    if not existing:
        return
    
    with zipfile.ZipFile(DATA_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in existing:
            zf.write(f)
            os.remove(f)
    print(f"Compressed to {DATA_FILE}")


def decompress_from_dat():
    if not os.path.exists(DATA_FILE):
        return False
    
    with zipfile.ZipFile(DATA_FILE, 'r') as zf:
        zf.extractall()
    print(f"Decompressed {DATA_FILE}")
    return True


def save_pickle(students, courses):
    data = {
        'students': [{'id': s.id, 'name': s.name, 'dob': s.dob, 'marks': s.marks} for s in students],
        'courses': [{'id': c.id, 'name': c.name, 'credits': c.credits} for c in courses]
    }
    
    with zipfile.ZipFile(DATA_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("data.pkl", pickle.dumps(data))
    print(f"Saved pickle to {DATA_FILE}")


def load_pickle():
    students, courses = [], []
    
    if not os.path.exists(DATA_FILE):
        return students, courses
    
    try:
        with zipfile.ZipFile(DATA_FILE, 'r') as zf:
            if "data.pkl" in zf.namelist():
                data = pickle.loads(zf.read("data.pkl"))
                
                for d in data['students']:
                    s = Student(d['id'], d['name'], d['dob'])
                    for cid, m in d['marks'].items():
                        s.set_mark(cid, m)
                    students.append(s)
                
                for d in data['courses']:
                    courses.append(Course(d['id'], d['name'], d['credits']))
                
                print(f"Loaded pickle from {DATA_FILE}")
    except:
        pass
    
    return students, courses


class CursesUI:
    MENU = [
        "1. Input Students",
        "2. Input Courses",
        "3. Input Marks",
        "4. List Students",
        "5. List Courses",
        "6. Show Marks",
        "7. Sort by GPA",
        "8. Save (txt+zip)",
        "9. Save (pickle)",
        "0. Exit"
    ]
    
    def __init__(self, students, courses):
        self.students = students
        self.courses = courses
        self.sel = 0
    
    def draw(self, scr):
        scr.clear()
        h, w = scr.getmaxyx()
        
        title = "STUDENT MARK MANAGEMENT"
        scr.addstr(1, (w-len(title))//2, title, curses.A_BOLD)
        
        for i, item in enumerate(self.MENU):
            x = (w - len(item)) // 2
            if i == self.sel:
                scr.attron(curses.A_REVERSE)
            scr.addstr(3 + i, x, item)
            if i == self.sel:
                scr.attroff(curses.A_REVERSE)
        
        stats = f"[{len(self.students)} students | {len(self.courses)} courses]"
        scr.addstr(h-2, (w-len(stats))//2, stats, curses.A_DIM)
        scr.refresh()
    
    def console_mode(self, scr, func):
        curses.endwin()
        func()
        input("\nPress Enter...")
        scr = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        scr.keypad(True)
        return scr
    
    def run(self):
        scr = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        scr.keypad(True)
        
        try:
            while True:
                self.draw(scr)
                key = scr.getch()
                
                if key == curses.KEY_UP:
                    self.sel = (self.sel - 1) % len(self.MENU)
                elif key == curses.KEY_DOWN:
                    self.sel = (self.sel + 1) % len(self.MENU)
                elif key in [10, 13, curses.KEY_ENTER]:
                    if self.sel == 0:
                        scr = self.console_mode(scr, lambda: input_students(self.students))
                    elif self.sel == 1:
                        scr = self.console_mode(scr, lambda: input_courses(self.courses))
                    elif self.sel == 2:
                        scr = self.console_mode(scr, lambda: input_marks(self.students, self.courses))
                    elif self.sel == 3:
                        scr = self.console_mode(scr, lambda: list_students(self.students))
                    elif self.sel == 4:
                        scr = self.console_mode(scr, lambda: list_courses(self.courses))
                    elif self.sel == 5:
                        scr = self.console_mode(scr, lambda: show_marks(self.students, self.courses))
                    elif self.sel == 6:
                        scr = self.console_mode(scr, lambda: sort_by_gpa(self.students, self.courses))
                    elif self.sel == 7:
                        scr = self.console_mode(scr, lambda: self.save_txt())
                    elif self.sel == 8:
                        scr = self.console_mode(scr, lambda: save_pickle(self.students, self.courses))
                    elif self.sel == 9:
                        break
                elif key == ord('0'):
                    break
        finally:
            curses.endwin()
    
    def save_txt(self):
        write_students_txt(self.students)
        write_courses_txt(self.courses)
        write_marks_txt(self.students)
        compress_to_dat()


def load_data():
    students, courses = load_pickle()
    if students or courses:
        return students, courses
    
    if os.path.exists(DATA_FILE):
        decompress_from_dat()
    
    students = load_students_txt()
    courses = load_courses_txt()
    load_marks_txt(students)
    
    if students:
        print(f"Loaded {len(students)} students, {len(courses)} courses from txt")
    
    return students, courses


def main():
    print("Loading data...")
    students, courses = load_data()
    
    print("\nStudent Mark Management System")
    print("Using curses UI...")
    
    try:
        ui = CursesUI(students, courses)
        ui.run()
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nGoodbye!")


if __name__ == "__main__":
    main()
