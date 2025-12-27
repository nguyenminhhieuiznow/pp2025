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

    def input(self):
        self._id = input("ID: ").strip()
        self._name = input("Ten: ").strip()
        self._dob = input("NgaySinh: ").strip()

    def __str__(self):
        return f"{self._id:<10} {self._name:<15} {self._dob:<12}"


class Course:
    def __init__(self, course_id="", name=""):
        self._id = course_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def input(self):
        self._id = input("ID: ").strip()
        self._name = input("Ten: ").strip()

    def __str__(self):
        return f"{self._id:<10} {self._name:<20}"


class MarkSheet:
    def __init__(self):
        self._students = []
        self._courses = []
        self._marks = {}

    def _input_number(self, prompt):
        while True:
            try:
                num = int(input(prompt))
                if num > 0:
                    return num
                print("Nhap so duong.")
            except ValueError:
                print("Nhap so.")

    def input_students(self):
        num = self._input_number("So luong sinh vien: ")
        for i in range(num):
            print(f"\n-- SV {i + 1} --")
            s = Student()
            s.input()
            self._students.append(s)
        print(f"\nDa them {num} SV.")

    def input_courses(self):
        num = self._input_number("So luong mon hoc: ")
        for i in range(num):
            print(f"\n-- Mon {i + 1} --")
            c = Course()
            c.input()
            self._courses.append(c)
            self._marks[c.id] = {}
        print(f"\nDa them {num} mon.")

    def _find_course(self, course_id):
        for c in self._courses:
            if c.id == course_id:
                return c
        return None

    def input_marks(self):
        if not self._courses:
            print("Chua co mon hoc.")
            return
        if not self._students:
            print("Chua co sinh vien.")
            return

        self.list_courses()
        course_id = input("\nNhap ID mon: ").strip()
        course = self._find_course(course_id)

        if not course:
            print("Khong tim thay.")
            return

        print(f"\nNhap diem mon: {course.name}")

        for s in self._students:
            while True:
                try:
                    mark = float(input(f"{s.name} ({s.id}): "))
                    if 0 <= mark <= 20:
                        self._marks[course_id][s.id] = mark
                        break
                    print("Diem 0-20.")
                except ValueError:
                    print("Nhap so.")

        print("\nDa luu diem.")

    def list_courses(self):
        if not self._courses:
            print("Chua co mon hoc.")
            return

        print(f"\n{'ID':<10} {'Ten':<20}")
        print("-" * 30)
        for c in self._courses:
            print(c)

    def list_students(self):
        if not self._students:
            print("Chua co sinh vien.")
            return

        print(f"\n{'ID':<10} {'Ten':<15} {'NgaySinh':<12}")
        print("-" * 40)
        for s in self._students:
            print(s)

    def show_marks(self):
        if not self._courses:
            print("Chua co mon hoc.")
            return

        self.list_courses()
        course_id = input("\nNhap ID mon: ").strip()
        course = self._find_course(course_id)

        if not course:
            print("Khong tim thay.")
            return

        if course_id not in self._marks or not self._marks[course_id]:
            print(f"Chua co diem mon: {course.name}")
            return

        print(f"\nDiem mon: {course.name}")
        print(f"{'ID':<10} {'Ten':<15} {'Diem':<6}")
        print("-" * 35)

        for s in self._students:
            if s.id in self._marks[course_id]:
                print(f"{s.id:<10} {s.name:<15} {self._marks[course_id][s.id]:<6.1f}")


def display_menu():
    print("\n===== QUAN LY DIEM (OOP) =====")
    print("1. Nhap SV")
    print("2. Nhap mon")
    print("3. Nhap diem")
    print("4. DS mon")
    print("5. DS SV")
    print("6. Xem diem")
    print("0. Thoat")


def main():
    ms = MarkSheet()

    while True:
        display_menu()
        choice = input("Chon: ").strip()

        if choice == "1":
            ms.input_students()
        elif choice == "2":
            ms.input_courses()
        elif choice == "3":
            ms.input_marks()
        elif choice == "4":
            ms.list_courses()
        elif choice == "5":
            ms.list_students()
        elif choice == "6":
            ms.show_marks()
        elif choice == "0":
            print("Tam biet!")
            break
        else:
            print("Chon lai.")


if __name__ == "__main__":
    main()
