from math import log
import math
# This program demonstrates various Python features and syntax

# Basic variable assignment and string manipulation
my_name = "Alice"
print(f"Hello, {my_name}!")
print(log(2.0, 3.0))
print(math.pow(2, 3))

# String concatenation 
a = "Hello"
b = "World"
print(a + b)
print("Goodbye" + "World")
v = a[1] + b[2]
print(v)

p = 1337

list1 = [1, 2, 3]
list2 = [2, 3, 4]
v = list1[0] + list2[1]
print(v)

# Lists and list comprehensions
my_list = [1, 2, 3, 4, 5]
squared_list = [x**2 for x in my_list]
print(squared_list)

# Conditional statements and loops
for i in range(10):
    if i % 2 == 0:
        print(f"{i} is even")
    else:
        print(f"{i} is odd")

# Functions and recursion
def factorial(n: int):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
print(factorial(5))

# Classes and inheritance
class Animal:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def __init__(self, name, color, breed):
        super().__init__(name, color)
        self.breed = breed

    def speak(self):
        print("Woof!")
        return "Bark!"

class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, color)

    def speak(self):
        print("Meow!")

class Person:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        self.pets.append(pet)

    def show_pets(self):
        for pet in self.pets:
            print(pet.name, pet.color, pet.__class__.__name__)

my_dog = Dog("Fido", "brown", "Golden Retriever")
my_cat = Cat("Whiskers", "gray")
my_person = Person("Bob")
my_person.add_pet(my_dog)
my_person.add_pet(my_cat)
my_person.show_pets()


# Iterators
my_iterator = iter(my_list)
print(next(my_iterator))

# Lambda functions
add = lambda x, y: x + y
print(add(2, 3))

# Generators and iterables
def squares(n):
    for i in range(n):
        yield i**2

my_generator = squares(5)
for i in my_generator:
    print(i)

# Exceptions
try:
    a = 1 / 0
except ZeroDivisionError:
    print("Division by zero is not allowed.")

# Context managers
with open("test.txt", "w") as f:
    f.write("Hello, world!")

# Lambdas and higher-order functions
def apply(func, x):
    return func(x)

def test(i, x):
    i += x
    return i

print(apply(lambda x: x**2, 3))
x = 135743895743875
y = 2 
z = 3
i = (x + y) - (z + 12 & z) ^ 13 
j = i + x - z + 133
print(j)
print(i)
def x():
    string = "abcdefghijklmnop"
    return string
x()
