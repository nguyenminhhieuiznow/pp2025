import math
import numpy as np
import curses


class Student:
    def __init__(self, student_id="", name="", dob=""):
        self._id = student_id
        self._name = name
        self._dob = dob

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def dob(self):
        return self._dob

    def input(self, stdscr):
        curses.echo()
        stdscr.addstr("ID: ")
        stdscr.refresh()
        self._id = stdscr.getstr().decode().strip()
        stdscr.addstr("Ten: ")
        stdscr.refresh()
        self._name = stdscr.getstr().decode().strip()
        stdscr.addstr("NgaySinh: ")
        stdscr.refresh()
        self._dob = stdscr.getstr().decode().strip()
        curses.noecho()

    def __str__(self):
        return f"{self._id:<10} {self._name:<15} {self._dob:<12}"


class Course:
    def __init__(self, course_id="", name="", credit=0):
        self._id = course_id
        self._name = name
        self._credit = credit

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def credit(self):
        return self._credit

    def input(self, stdscr):
        curses.echo()
        stdscr.addstr("ID: ")
        stdscr.refresh()
        self._id = stdscr.getstr().decode().strip()
        stdscr.addstr("Ten: ")
        stdscr.refresh()
        self._name = stdscr.getstr().decode().strip()
        while True:
            stdscr.addstr("So tin chi: ")
            stdscr.refresh()
            try:
                self._credit = int(stdscr.getstr().decode().strip())
                if self._credit > 0:
                    break
            except ValueError:
                pass
            stdscr.addstr("Nhap so duong.\n")
        curses.noecho()

    def __str__(self):
        return f"{self._id:<10} {self._name:<20} {self._credit:<5}"


class MarkSheet:
    def __init__(self):
        self._students = []
        self._courses = []
        self._marks = {}

    def _input_number(self, stdscr, prompt):
        curses.echo()
        while True:
            stdscr.addstr(prompt)
            stdscr.refresh()
            try:
                num = int(stdscr.getstr().decode().strip())
                if num > 0:
                    curses.noecho()
                    return num
            except ValueError:
                pass
            stdscr.addstr("Nhap so duong.\n")

    def input_students(self, stdscr):
        num = self._input_number(stdscr, "So luong sinh vien: ")
        for i in range(num):
            stdscr.addstr(f"\n-- SV {i + 1} --\n")
            s = Student()
            s.input(stdscr)
            self._students.append(s)
        stdscr.addstr(f"\nDa them {num} SV.\n")
        stdscr.refresh()
        stdscr.getch()

    def input_courses(self, stdscr):
        num = self._input_number(stdscr, "So luong mon hoc: ")
        for i in range(num):
            stdscr.addstr(f"\n-- Mon {i + 1} --\n")
            c = Course()
            c.input(stdscr)
            self._courses.append(c)
            self._marks[c.id] = {}
        stdscr.addstr(f"\nDa them {num} mon.\n")
        stdscr.refresh()
        stdscr.getch()

    def _find_course(self, course_id):
        for c in self._courses:
            if c.id == course_id:
                return c
        return None

    def input_marks(self, stdscr):
        if not self._courses:
            stdscr.addstr("Chua co mon hoc.\n")
            stdscr.getch()
            return
        if not self._students:
            stdscr.addstr("Chua co sinh vien.\n")
            stdscr.getch()
            return

        self.list_courses(stdscr, wait=False)
        curses.echo()
        stdscr.addstr("\nNhap ID mon: ")
        stdscr.refresh()
        course_id = stdscr.getstr().decode().strip()
        course = self._find_course(course_id)

        if not course:
            stdscr.addstr("Khong tim thay.\n")
            stdscr.getch()
            curses.noecho()
            return

        stdscr.addstr(f"\nNhap diem mon: {course.name}\n")

        for s in self._students:
            while True:
                stdscr.addstr(f"{s.name} ({s.id}): ")
                stdscr.refresh()
                try:
                    mark = float(stdscr.getstr().decode().strip())
                    if 0 <= mark <= 20:
                        mark = math.floor(mark * 10) / 10
                        self._marks[course_id][s.id] = mark
                        break
                    stdscr.addstr("Diem 0-20.\n")
                except ValueError:
                    stdscr.addstr("Nhap so.\n")

        curses.noecho()
        stdscr.addstr("\nDa luu diem.\n")
        stdscr.refresh()
        stdscr.getch()

    def list_courses(self, stdscr, wait=True):
        if not self._courses:
            stdscr.addstr("Chua co mon hoc.\n")
            if wait:
                stdscr.getch()
            return

        stdscr.addstr(f"\n{'ID':<10} {'Ten':<20} {'TC':<5}\n")
        stdscr.addstr("-" * 35 + "\n")
        for c in self._courses:
            stdscr.addstr(str(c) + "\n")
        stdscr.refresh()
        if wait:
            stdscr.getch()

    def list_students(self, stdscr):
        if not self._students:
            stdscr.addstr("Chua co sinh vien.\n")
            stdscr.getch()
            return

        stdscr.addstr(f"\n{'ID':<10} {'Ten':<15} {'NgaySinh':<12}\n")
        stdscr.addstr("-" * 40 + "\n")
        for s in self._students:
            stdscr.addstr(str(s) + "\n")
        stdscr.refresh()
        stdscr.getch()

    def show_marks(self, stdscr):
        if not self._courses:
            stdscr.addstr("Chua co mon hoc.\n")
            stdscr.getch()
            return

        self.list_courses(stdscr, wait=False)
        curses.echo()
        stdscr.addstr("\nNhap ID mon: ")
        stdscr.refresh()
        course_id = stdscr.getstr().decode().strip()
        curses.noecho()
        course = self._find_course(course_id)

        if not course:
            stdscr.addstr("Khong tim thay.\n")
            stdscr.getch()
            return

        if course_id not in self._marks or not self._marks[course_id]:
            stdscr.addstr(f"Chua co diem mon: {course.name}\n")
            stdscr.getch()
            return

        stdscr.addstr(f"\nDiem mon: {course.name}\n")
        stdscr.addstr(f"{'ID':<10} {'Ten':<15} {'Diem':<6}\n")
        stdscr.addstr("-" * 35 + "\n")

        for s in self._students:
            if s.id in self._marks[course_id]:
                stdscr.addstr(f"{s.id:<10} {s.name:<15} {self._marks[course_id][s.id]:<6.1f}\n")
        stdscr.refresh()
        stdscr.getch()

    def calculate_gpa(self, student_id):
        marks_list = []
        credits_list = []

        for c in self._courses:
            if c.id in self._marks and student_id in self._marks[c.id]:
                marks_list.append(self._marks[c.id][student_id])
                credits_list.append(c.credit)

        if not marks_list:
            return 0.0

        marks_arr = np.array(marks_list)
        credits_arr = np.array(credits_list)
        return np.sum(marks_arr * credits_arr) / np.sum(credits_arr)

    def show_gpa(self, stdscr):
        if not self._students:
            stdscr.addstr("Chua co sinh vien.\n")
            stdscr.getch()
            return

        self.list_students(stdscr)
        curses.echo()
        stdscr.addstr("Nhap ID SV: ")
        stdscr.refresh()
        student_id = stdscr.getstr().decode().strip()
        curses.noecho()

        student = None
        for s in self._students:
            if s.id == student_id:
                student = s
                break

        if not student:
            stdscr.addstr("Khong tim thay.\n")
            stdscr.getch()
            return

        gpa = self.calculate_gpa(student_id)
        stdscr.addstr(f"\nGPA cua {student.name}: {gpa:.2f}\n")
        stdscr.refresh()
        stdscr.getch()

    def sort_by_gpa(self, stdscr):
        if not self._students:
            stdscr.addstr("Chua co sinh vien.\n")
            stdscr.getch()
            return

        gpa_list = [(s, self.calculate_gpa(s.id)) for s in self._students]
        gpa_list.sort(key=lambda x: x[1], reverse=True)

        stdscr.addstr(f"\n{'ID':<10} {'Ten':<15} {'GPA':<6}\n")
        stdscr.addstr("-" * 35 + "\n")
        for s, gpa in gpa_list:
            stdscr.addstr(f"{s.id:<10} {s.name:<15} {gpa:<6.2f}\n")
        stdscr.refresh()
        stdscr.getch()


def main(stdscr):
    curses.curs_set(1)
    stdscr.clear()

    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    ms = MarkSheet()

    while True:
        stdscr.clear()
        if curses.has_colors():
            stdscr.attron(curses.color_pair(1))
        stdscr.addstr("===== QUAN LY DIEM (OOP + MATH) =====\n")
        if curses.has_colors():
            stdscr.attroff(curses.color_pair(1))

        stdscr.addstr("1. Nhap SV\n")
        stdscr.addstr("2. Nhap mon\n")
        stdscr.addstr("3. Nhap diem\n")
        stdscr.addstr("4. DS mon\n")
        stdscr.addstr("5. DS SV\n")
        stdscr.addstr("6. Xem diem\n")
        stdscr.addstr("7. Xem GPA\n")
        stdscr.addstr("8. Xep hang GPA\n")
        stdscr.addstr("0. Thoat\n")

        if curses.has_colors():
            stdscr.attron(curses.color_pair(2))
        stdscr.addstr("\nChon: ")
        if curses.has_colors():
            stdscr.attroff(curses.color_pair(2))

        stdscr.refresh()
        choice = stdscr.getch()

        stdscr.clear()

        if choice == ord('1'):
            ms.input_students(stdscr)
        elif choice == ord('2'):
            ms.input_courses(stdscr)
        elif choice == ord('3'):
            ms.input_marks(stdscr)
        elif choice == ord('4'):
            ms.list_courses(stdscr)
        elif choice == ord('5'):
            ms.list_students(stdscr)
        elif choice == ord('6'):
            ms.show_marks(stdscr)
        elif choice == ord('7'):
            ms.show_gpa(stdscr)
        elif choice == ord('8'):
            ms.sort_by_gpa(stdscr)
        elif choice == ord('0'):
            break


if __name__ == "__main__":
    curses.wrapper(main)
