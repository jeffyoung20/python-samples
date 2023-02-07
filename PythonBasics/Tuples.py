class Person:
    _id = 0
    def __init__(self, fName, lName):
        self.fName = fName
        self.lName = lName
        Person._id = Person._id + 1
        self.id = Person._id

    def GetPersonInfo(self):
        return self.id, self.fName, self.lName

    def __str__(self) -> str:
        return f"ID:  {self.id},  Name: {self.fName} {self.lName}"

p1 = Person("Jeff","Young")
print(p1)

p2 = Person("George", "Washington")
print(p2)

id, fName, lName = p2.GetPersonInfo()
print(id)
print(fName)
print(lName)

#Add extra property dynamcally to person object
p2.age = 10
print(p2.age)


