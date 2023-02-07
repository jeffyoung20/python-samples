
class PersonWrong:
    firstName = "Jim"
    lastName = "Brown"

    def __init__(self, firstName: str, lastName: str) -> None:
        firstName = firstName
        lastName = lastName

    def printNameGlobal(self) -> str:
        print(PersonWrong.firstName, PersonWrong.lastName)

    def printNameInternal(self) -> str:
        print(self.firstName, self.lastName)

class Person:
    firstName = "John"
    lastName = "Smith"

    def __init__(self, firstName: str, lastName: str) -> None:
        self.firstName = firstName
        self.lastName = lastName

    def printNameGlobal(self) -> str:
        print(Person.firstName, Person.lastName)

    def printNameInternal(self) -> str:
        print(self.firstName, self.lastName)


print("Start")

# Person 1
# p1 = PersonWrong()
# p1.printNameInternal() #Jim Brown
# p1.printNameGlobal() #Jim Brown

# Person 1
p1 = PersonWrong("Jeff", "Young")
p1.printNameInternal() #Jim Brown
p1.printNameGlobal() #Jim Brown


# Person 2
p2 = Person("Jeff", "Young")
p2.printNameGlobal() #John Smith
p2.printNameInternal() #Jeff Young

p2.firstName = "Jeff2"
p2.printNameGlobal() #John Smith
p2.printNameInternal()  #Jeff2 Young

Person.firstName = "John2"
p2.printNameGlobal() #John2 Smith
p2.printNameInternal()  #Jeff2 Young


print("the end")



