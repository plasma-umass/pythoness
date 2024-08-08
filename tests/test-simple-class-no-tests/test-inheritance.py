import pythoness



class Person:
  
  @pythoness.spec("initializes the first and lastname of Person")
  def __init__(self, fname, lname):
    ""

  @pythoness.spec("prints first and lastname in the format (firstname, lastname)", related_objs=['cls'])
  def printname(self):
    ""

  @pythoness.spec("get the fname of a Person", related_objs=[__init__])
  def get_fname(self):
    ""

  @pythoness.spec("get the lname of a Person", related_objs=[__init__])
  def get_lname(self):
    ""

class Student(Person):
  
  @pythoness.spec("initializes the person superclass with firstname and lastname", related_objs=[Person])
  def __init__(self, fname, lname):
    ""

  @pythoness.spec("prints first and lastname in the format (firstname, lastname)", related_objs=['cls'])
  def printname2(self):
    ""
    
if __name__ == "__main__":
  student = Student('jane', 'doe')
  student.printname()
  print(student.get_fname())
  student.printname2()
  print(Student('john', 'doe').get_fname())