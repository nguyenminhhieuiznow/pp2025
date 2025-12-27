class Student:
    def __init__(self, student_id="", name="", dob=""):
        self._id = student_id
        self._name = name
        self._dob = dob

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def dob(self):
        return self._dob

    @dob.setter
    def dob(self, value):
        self._dob = value

    def __str__(self):
        return f"{self._id:<10} {self._name:<15} {self._dob:<12}"
