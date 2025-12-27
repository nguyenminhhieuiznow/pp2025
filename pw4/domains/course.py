class Course:
    def __init__(self, course_id="", name="", credit=0):
        self._id = course_id
        self._name = name
        self._credit = credit

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
    def credit(self):
        return self._credit

    @credit.setter
    def credit(self, value):
        self._credit = value

    def __str__(self):
        return f"{self._id:<10} {self._name:<20} {self._credit:<5}"
