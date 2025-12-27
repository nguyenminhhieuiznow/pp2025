import numpy as np


class MarkSheet:
    def __init__(self):
        self._students = []
        self._courses = []
        self._marks = {}

    @property
    def students(self):
        return self._students

    @property
    def courses(self):
        return self._courses

    @property
    def marks(self):
        return self._marks

    def add_student(self, student):
        self._students.append(student)

    def add_course(self, course):
        self._courses.append(course)
        self._marks[course.id] = {}

    def set_mark(self, course_id, student_id, mark):
        self._marks[course_id][student_id] = mark

    def find_course(self, course_id):
        for c in self._courses:
            if c.id == course_id:
                return c
        return None

    def find_student(self, student_id):
        for s in self._students:
            if s.id == student_id:
                return s
        return None

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

    def get_sorted_by_gpa(self):
        gpa_list = [(s, self.calculate_gpa(s.id)) for s in self._students]
        gpa_list.sort(key=lambda x: x[1], reverse=True)
        return gpa_list
