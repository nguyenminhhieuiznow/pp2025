import curses


def init_colors():
    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)


def print_title(stdscr, title):
    if curses.has_colors():
        stdscr.attron(curses.color_pair(1))
    stdscr.addstr(f"===== {title} =====\n")
    if curses.has_colors():
        stdscr.attroff(curses.color_pair(1))


def print_menu(stdscr):
    print_title(stdscr, "QUAN LY DIEM")
    stdscr.addstr("1. Nhap SV\n")
    stdscr.addstr("2. Nhap mon\n")
    stdscr.addstr("3. Nhap diem\n")
    stdscr.addstr("4. DS mon\n")
    stdscr.addstr("5. DS SV\n")
    stdscr.addstr("6. Xem diem\n")
    stdscr.addstr("7. Xem GPA\n")
    stdscr.addstr("8. Xep hang GPA\n")
    stdscr.addstr("0. Thoat\n")
    print_prompt(stdscr, "\nChon: ")


def print_prompt(stdscr, text):
    if curses.has_colors():
        stdscr.attron(curses.color_pair(2))
    stdscr.addstr(text)
    if curses.has_colors():
        stdscr.attroff(curses.color_pair(2))
    stdscr.refresh()


def print_success(stdscr, text):
    if curses.has_colors():
        stdscr.attron(curses.color_pair(3))
    stdscr.addstr(text + "\n")
    if curses.has_colors():
        stdscr.attroff(curses.color_pair(3))
    stdscr.refresh()


def print_courses(stdscr, courses):
    if not courses:
        stdscr.addstr("Chua co mon hoc.\n")
        return

    stdscr.addstr(f"\n{'ID':<10} {'Ten':<20} {'TC':<5}\n")
    stdscr.addstr("-" * 35 + "\n")
    for c in courses:
        stdscr.addstr(str(c) + "\n")
    stdscr.refresh()


def print_students(stdscr, students):
    if not students:
        stdscr.addstr("Chua co sinh vien.\n")
        return

    stdscr.addstr(f"\n{'ID':<10} {'Ten':<15} {'NgaySinh':<12}\n")
    stdscr.addstr("-" * 40 + "\n")
    for s in students:
        stdscr.addstr(str(s) + "\n")
    stdscr.refresh()


def print_marks(stdscr, course_name, students, marks, course_id):
    stdscr.addstr(f"\nDiem mon: {course_name}\n")
    stdscr.addstr(f"{'ID':<10} {'Ten':<15} {'Diem':<6}\n")
    stdscr.addstr("-" * 35 + "\n")

    for s in students:
        if s.id in marks[course_id]:
            stdscr.addstr(f"{s.id:<10} {s.name:<15} {marks[course_id][s.id]:<6.1f}\n")
    stdscr.refresh()


def print_gpa_list(stdscr, gpa_list):
    stdscr.addstr(f"\n{'ID':<10} {'Ten':<15} {'GPA':<6}\n")
    stdscr.addstr("-" * 35 + "\n")
    for s, gpa in gpa_list:
        stdscr.addstr(f"{s.id:<10} {s.name:<15} {gpa:<6.2f}\n")
    stdscr.refresh()


def wait_key(stdscr):
    stdscr.getch()
