from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

person = Person(name="Ram", age=30)
print(person.name, person.age)