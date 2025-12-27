import math
import curses
from domains import Student, Course


def input_number(stdscr, prompt):
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


def input_student(stdscr):
    s = Student()
    curses.echo()
    stdscr.addstr("ID: ")
    stdscr.refresh()
    s.id = stdscr.getstr().decode().strip()
    stdscr.addstr("Ten: ")
    stdscr.refresh()
    s.name = stdscr.getstr().decode().strip()
    stdscr.addstr("NgaySinh: ")
    stdscr.refresh()
    s.dob = stdscr.getstr().decode().strip()
    curses.noecho()
    return s


def input_course(stdscr):
    c = Course()
    curses.echo()
    stdscr.addstr("ID: ")
    stdscr.refresh()
    c.id = stdscr.getstr().decode().strip()
    stdscr.addstr("Ten: ")
    stdscr.refresh()
    c.name = stdscr.getstr().decode().strip()
    while True:
        stdscr.addstr("So tin chi: ")
        stdscr.refresh()
        try:
            c.credit = int(stdscr.getstr().decode().strip())
            if c.credit > 0:
                break
        except ValueError:
            pass
        stdscr.addstr("Nhap so duong.\n")
    curses.noecho()
    return c


def input_mark(stdscr, student_name, student_id):
    curses.echo()
    while True:
        stdscr.addstr(f"{student_name} ({student_id}): ")
        stdscr.refresh()
        try:
            mark = float(stdscr.getstr().decode().strip())
            if 0 <= mark <= 20:
                curses.noecho()
                return math.floor(mark * 10) / 10
            stdscr.addstr("Diem 0-20.\n")
        except ValueError:
            stdscr.addstr("Nhap so.\n")


def input_string(stdscr, prompt):
    curses.echo()
    stdscr.addstr(prompt)
    stdscr.refresh()
    result = stdscr.getstr().decode().strip()
    curses.noecho()
    return result
