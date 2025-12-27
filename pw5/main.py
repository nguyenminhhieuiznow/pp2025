import curses
from domains import MarkSheet
import input as inp
import output as out
import storage


def input_students(stdscr, ms):
    num = inp.input_number(stdscr, "So luong sinh vien: ")
    for i in range(num):
        stdscr.addstr(f"\n-- SV {i + 1} --\n")
        s = inp.input_student(stdscr)
        ms.add_student(s)
    storage.save_students(ms.students)
    out.print_success(stdscr, f"\nDa them {num} SV.")
    out.wait_key(stdscr)


def input_courses(stdscr, ms):
    num = inp.input_number(stdscr, "So luong mon hoc: ")
    for i in range(num):
        stdscr.addstr(f"\n-- Mon {i + 1} --\n")
        c = inp.input_course(stdscr)
        ms.add_course(c)
    storage.save_courses(ms.courses)
    out.print_success(stdscr, f"\nDa them {num} mon.")
    out.wait_key(stdscr)


def input_marks(stdscr, ms):
    if not ms.courses:
        stdscr.addstr("Chua co mon hoc.\n")
        out.wait_key(stdscr)
        return
    if not ms.students:
        stdscr.addstr("Chua co sinh vien.\n")
        out.wait_key(stdscr)
        return

    out.print_courses(stdscr, ms.courses)
    course_id = inp.input_string(stdscr, "\nNhap ID mon: ")
    course = ms.find_course(course_id)

    if not course:
        stdscr.addstr("Khong tim thay.\n")
        out.wait_key(stdscr)
        return

    stdscr.addstr(f"\nNhap diem mon: {course.name}\n")

    for s in ms.students:
        mark = inp.input_mark(stdscr, s.name, s.id)
        ms.set_mark(course_id, s.id, mark)

    storage.save_marks(ms.marks)
    out.print_success(stdscr, "\nDa luu diem.")
    out.wait_key(stdscr)


def list_courses(stdscr, ms):
    out.print_courses(stdscr, ms.courses)
    out.wait_key(stdscr)


def list_students(stdscr, ms):
    out.print_students(stdscr, ms.students)
    out.wait_key(stdscr)


def show_marks(stdscr, ms):
    if not ms.courses:
        stdscr.addstr("Chua co mon hoc.\n")
        out.wait_key(stdscr)
        return

    out.print_courses(stdscr, ms.courses)
    course_id = inp.input_string(stdscr, "\nNhap ID mon: ")
    course = ms.find_course(course_id)

    if not course:
        stdscr.addstr("Khong tim thay.\n")
        out.wait_key(stdscr)
        return

    if course_id not in ms.marks or not ms.marks[course_id]:
        stdscr.addstr(f"Chua co diem mon: {course.name}\n")
        out.wait_key(stdscr)
        return

    out.print_marks(stdscr, course.name, ms.students, ms.marks, course_id)
    out.wait_key(stdscr)


def show_gpa(stdscr, ms):
    if not ms.students:
        stdscr.addstr("Chua co sinh vien.\n")
        out.wait_key(stdscr)
        return

    out.print_students(stdscr, ms.students)
    student_id = inp.input_string(stdscr, "Nhap ID SV: ")
    student = ms.find_student(student_id)

    if not student:
        stdscr.addstr("Khong tim thay.\n")
        out.wait_key(stdscr)
        return

    gpa = ms.calculate_gpa(student_id)
    out.print_success(stdscr, f"\nGPA cua {student.name}: {gpa:.2f}")
    out.wait_key(stdscr)


def sort_by_gpa(stdscr, ms):
    if not ms.students:
        stdscr.addstr("Chua co sinh vien.\n")
        out.wait_key(stdscr)
        return

    gpa_list = ms.get_sorted_by_gpa()
    out.print_gpa_list(stdscr, gpa_list)
    out.wait_key(stdscr)


def select_compression(stdscr):
    stdscr.clear()
    out.print_title(stdscr, "CHON PHUONG THUC NEN")
    stdscr.addstr("1. zlib (mac dinh)\n")
    stdscr.addstr("2. bz2\n")
    stdscr.addstr("3. lzma\n")
    out.print_prompt(stdscr, "\nChon: ")
    choice = stdscr.getch()

    if choice == ord('2'):
        return "2"
    elif choice == ord('3'):
        return "3"
    return "1"


def main(stdscr):
    curses.curs_set(1)
    out.init_colors()
    ms = MarkSheet()

    storage.decompress_data()
    students = storage.load_students()
    courses = storage.load_courses()
    marks = storage.load_marks()
    ms.load_data(students, courses, marks)

    while True:
        stdscr.clear()
        out.print_menu(stdscr)
        choice = stdscr.getch()
        stdscr.clear()

        if choice == ord('1'):
            input_students(stdscr, ms)
        elif choice == ord('2'):
            input_courses(stdscr, ms)
        elif choice == ord('3'):
            input_marks(stdscr, ms)
        elif choice == ord('4'):
            list_courses(stdscr, ms)
        elif choice == ord('5'):
            list_students(stdscr, ms)
        elif choice == ord('6'):
            show_marks(stdscr, ms)
        elif choice == ord('7'):
            show_gpa(stdscr, ms)
        elif choice == ord('8'):
            sort_by_gpa(stdscr, ms)
        elif choice == ord('0'):
            break

    method = select_compression(stdscr)
    method_name = storage.compress_data(method)
    stdscr.clear()
    out.print_success(stdscr, f"Da nen bang {method_name}")
    out.wait_key(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
