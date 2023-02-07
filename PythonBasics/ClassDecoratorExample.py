from dataclasses import dataclass, asdict, field

@dataclass
class Person:
    firstName: str = "Joe"
    lastName: str = "Biden"
    middleName: str = field(default="", compare=False)
    age: int = field(default=80, compare=False)


print("Start")

p1 = Person()
print(p1)  #Person(firstName='Joe', lastName='Biden', middleName='', age=80)
print(asdict(p1))

p2 = Person("John","Adams")
print(p2)  #Person(firstName='John', lastName='Adams', middleName='', age=80)
print(asdict(p2))

p3 = Person("John","Adams", "Quincy")
print(p3)  #Person(firstName='John', lastName='Adams', middleName='Quincy', age=80)
print(asdict(p3))

p4 = Person("George", "Washington", age= 100)
print(p4)  #Person(firstName='George', lastName='Washington', middleName='', age=100)
print(asdict(p4))

if(p2 == p3):
    print(f"{p2} EQUAL {p3}") # Will be equal becuase middle name is not used in compare
else:
    print(f"{p2} NOT EQUAL {p3}")


print("End")



