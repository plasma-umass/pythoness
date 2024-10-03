import pythoness


class Student:
    "Class that stores a students name and an array of classes that they are taking"

    @pythoness.spec(
        """Constructor for a student, contains the students name (first and last) and classArr,
                        which is a list of what classes they are taking""",
        tests=[
            "Student('A B',['class1']).name == 'A B'",
            "Student('A',['class1']).classArr == ['class1']",
        ],
        verbose=True,
    )
    def __init__(self, name, classArr):
        """"""

    @pythoness.spec(
        "Returns the students name",
        tests=["Student('A',[]).get_name() == 'A'"],
        related_objs=[__init__],
        verbose=True,
    )
    def get_name(self):
        """"""

    @pythoness.spec(
        "Returns the student's last name",
        tests=["Student('A B',[]).get_last_name() == 'B'"],
        related_objs=[__init__],
        verbose=True,
    )
    def get_last_name(self):
        """"""

    @pythoness.spec(
        "Compares two students and returns true if their names are the same",
        tests=["Student('A',[]) == Student('A', ['class'])"],
        related_objs=[get_name],
        verbose=True,
    )
    def __eq__(self, other):
        """"""

    @pythoness.spec(
        "Returns true if the name of self comes before the name of other alphabetically",
        tests=[
            "Student('A',[]) < Student('B',[])",
            "not (Student('B',[]) < Student('A',[]))",
        ],
        related_objs=[get_name],
        verbose=True,
    )
    def __lt__(self, other):
        """"""

    @pythoness.spec(
        "Returns true if the name of self comes after the name of other alphabetically",
        tests=[
            "Student('B',[]) > Student('A',[])",
            "not (Student('A',[]) > Student('B',[]))",
        ],
        related_objs=[get_name],
        verbose=True,
    )
    def __gt__(self, other):
        """"""

    @pythoness.spec(
        "Returns the students classArr",
        tests=[
            "Student('A',['class1', 'class2']).get_class_arr() == ['class1','class2']"
        ],
        related_objs=[__init__],
        verbose=True,
    )
    def get_class_arr(self):
        """"""


class ExamScheduler:
    """A class that creates a final exam schedule for students, and gurantees that there are no conflicts
    for any student.
    Also can print out the schedule for each individual student, in alphabetical order by last name
    """

    @pythoness.spec(
        """Makes an undirected graph, where every node is a class that a student has,
                    and every edge connects classes that are taken by a common student.
                    Connects the graph of each student to the graph of all previous students""",
        related_objs=["cls", Student],
        verbose=True,
    )
    def make_class_graph(self, student: Student):
        """"""

    @pythoness.spec(
        "Stores the undirected graph of student objects",
        related_objs=["cls", Student],
        verbose=True,
    )
    def __init__(self):
        """"""

    @pythoness.spec(
        """Makes a final exam schedule by assigning each class into a time slot.
                    Makes more time slots as they become necessary.
                    Final exam schedule is stored as a dictionary""",
        related_objs=["cls", Student],
        verbose=True,
    )
    def make_schedule(self):
        """"""

    @pythoness.spec(
        "Given two lists, returns a boolean depending on if they have at least one string in common",
        related_objs=["cls", Student],
        verbose=True,
    )
    def include_common_string(v1: list, v2: list):
        """"""

    @pythoness.spec(
        "Makes a list of all neighbors of a given node in a graph",
        related_objs=["cls", Student],
        verbose=True,
    )
    def make_neighbors_vec(headNode) -> list:
        """"""

    @pythoness.spec(
        """Creates and prints a final exam schedule in the format:
                    
                    'Slot n: Class 1, Class 2, Class 3...'

                    for the students in student_list
                    """,
        related_objs=["cls", Student],
        verbose=True,
    )
    def print_schedule(self, student_list: list):
        """"""

    @pythoness.spec(
        "Converts a given list to a string of the form: 'element1, element2, element3...'",
        verbose=True,
    )
    def list_to_string(list):
        """"""


@pythoness.spec(
    """Reads a list of students and classes of the following format from filename:
                    FirstName LastName
                    Class1
                    Class2
                    Class3
                    Class4
                and makes a list of student objects out of them""",
    related_objs=["cls", Student],
    verbose=True,
)
def create_student_list(filename):
    """"""


if __name__ == "__main__":
    exam_scheduler = ExamScheduler()
    exam_scheduler.print_schedule(create_student_list("small.txt"))
