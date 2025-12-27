students = []
courses = []
marks = {}


def input_number(prompt):
    while True:
        try:
            num = int(input(prompt))
            if num > 0:
                return num
            print("Nhap so duong.")
        except ValueError:
            print("Nhap so.")


def input_student_info():
    student_id = input("ID: ").strip()
    name = input("Ten: ").strip()
    dob = input("NgaySinh: ").strip()
    return (student_id, name, dob)


def input_students():
    num = input_number("So luong sinh vien: ")
    for i in range(num):
        print(f"\n-- SV {i + 1} --")
        students.append(input_student_info())
    print(f"\nDa them {num} SV.")


def input_course_info():
    course_id = input("ID: ").strip()
    name = input("Ten: ").strip()
    return (course_id, name)


def input_courses():
    num = input_number("So luong mon hoc: ")
    for i in range(num):
        print(f"\n-- Mon {i + 1} --")
        course = input_course_info()
        courses.append(course)
        marks[course[0]] = {}
    print(f"\nDa them {num} mon.")


def find_course(course_id):
    for c in courses:
        if c[0] == course_id:
            return c
    return None


def input_marks_for_course():
    if not courses:
        print("Chua co mon hoc.")
        return
    if not students:
        print("Chua co sinh vien.")
        return

    list_courses()
    course_id = input("\nNhap ID mon: ").strip()
    course = find_course(course_id)

    if not course:
        print("Khong tim thay.")
        return

    print(f"\nNhap diem mon: {course[1]}")

    for student in students:
        while True:
            try:
                mark = float(input(f"{student[1]} ({student[0]}): "))
                if 0 <= mark <= 20:
                    marks[course_id][student[0]] = mark
                    break
                print("Diem 0-20.")
            except ValueError:
                print("Nhap so.")

    print("\nDa luu diem.")


def list_courses():
    if not courses:
        print("Chua co mon hoc.")
        return

    print(f"\n{'ID':<10} {'Ten':<20}")
    print("-" * 30)
    for c in courses:
        print(f"{c[0]:<10} {c[1]:<20}")


def list_students():
    if not students:
        print("Chua co sinh vien.")
        return

    print(f"\n{'ID':<10} {'Ten':<15} {'NgaySinh':<12}")
    print("-" * 40)
    for s in students:
        print(f"{s[0]:<10} {s[1]:<15} {s[2]:<12}")


def show_student_marks_for_course():
    if not courses:
        print("Chua co mon hoc.")
        return

    list_courses()
    course_id = input("\nNhap ID mon: ").strip()
    course = find_course(course_id)

    if not course:
        print("Khong tim thay.")
        return

    if course_id not in marks or not marks[course_id]:
        print(f"Chua co diem mon: {course[1]}")
        return

    print(f"\nDiem mon: {course[1]}")
    print(f"{'ID':<10} {'Ten':<15} {'Diem':<6}")
    print("-" * 35)

    for s in students:
        if s[0] in marks[course_id]:
            print(f"{s[0]:<10} {s[1]:<15} {marks[course_id][s[0]]:<6.1f}")


def display_menu():
    print("\n===== QUAN LY DIEM =====")
    print("1. Nhap SV")
    print("2. Nhap mon")
    print("3. Nhap diem")
    print("4. DS mon")
    print("5. DS SV")
    print("6. Xem diem")
    print("0. Thoat")


def main():
    while True:
        display_menu()
        choice = input("Chon: ").strip()

        if choice == "1":
            input_students()
        elif choice == "2":
            input_courses()
        elif choice == "3":
            input_marks_for_course()
        elif choice == "4":
            list_courses()
        elif choice == "5":
            list_students()
        elif choice == "6":
            show_student_marks_for_course()
        elif choice == "0":
            print("Tam biet!")
            break
        else:
            print("Chon lai.")


if __name__ == "__main__":
    main()
