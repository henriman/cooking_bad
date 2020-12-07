# datenbanken etc.
# website/gui etc.
import os
import hashlib
import functools
import getpass

"""
# TODO: rethink unit system
class Unit:
    # unit symbol?

    units = list()

    def __new__(cls, name: str) -> "Unit":
        unit_with_same_name = functools.reduce(
            lambda acc, u: acc if acc is not None else u if u.name == name else None, cls.units, None
        )

        if unit_with_same_name is not None:
            return unit_with_same_name
        else:
            return super().__new__(cls)

    def __init__(self, name: str):
        if name not in map(lambda unit: unit.name, self.units):
            self.name = name
            self.units.append(self)

    def __repr__(self):
        return f"Unit({self.name})"

    # TODO: class UnitError(Exception):

# TODO: use units / convert
class Quantity:
    def __init__(self, value: float, unit: Unit):
        self.value = value
        self.unit = unit

    def __neg__(self):
        return Quantity(-self.value, self.unit)

    def __add__(self, other: "Quantity") -> "Quantity":
        if not isinstance(other, Quantity):
            raise TypeError
        elif self.unit != other.unit:
            raise TypeError
        return Quantity(self.value + other.value, self.unit)
    def __sub__(self, other: "Quantity") -> "Quantity":
        return self + (-other)
    def __mul__(self, other):
        return Quantity(self.value * other, self.unit)
    def __truediv__(self, other):
        return self * (1 / other)

    def __repr__(self):
        return f"Quantity({self.value} {self.unit})"
"""

class Ingredient:
    # convert etc.
    def __init__(self, name: str, amount: int, unit: str):
        self.name = name
        self.amount = amount
        self.unit = unit

    def __str__(self):
        return f"{self.amount} {self.unit} {self.name}"

class IngredientList:
    def __init__(self, portions: int, ingredients: [Ingredient]):
        self.portions = portions
        self.ingredients = ingredients

    def __str__(self):
        portions = f"For {self.portions} portion(s):\n"
        ingredients = "\n".join(map(str, self.ingredients))
        return portions + ingredients

class Instruction:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

class Recipe:
    def __init__(self, name, ingredient_list: IngredientList, instructions: [Instruction]):
        self.name = name
        self.ingredient_list = ingredient_list
        self.instructions = instructions

    def __str__(self):
        instructions = "\n".join(map(lambda inst: f"{inst[0]}. {inst[1]}", enumerate(self.instructions, start=1)))
        return f"{self.name}\n\n{self.ingredient_list}\n\n{instructions}"

class Account:
    # verlinkung zu social media
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.authentication = self.Authentication(password)
        self.recipes = list()

    def add_recipe(self, recipe: Recipe):
        password = getpass.getpass("Please enter your password: ")

        if self.authentication.authenticate(password):
            self.recipes.append(recipe)
        else:
            print("Password incorrect, recipe was not added.")

    class Authentication:
        """A class for handling authentication of an account.

        To protect the passwords of the users, salted password hashing is employed,
        following the advice given here:
        https://crackstation.net/hashing-security.htm.
        The passwords are hashed using the `scrypt` algorithm:
        https://www.tarsnap.com/scrypt/scrypt.pdf.
        """

        # These values are taken from the original paper.
        n = 2**14
        r = 8
        p = 1

        def __init__(self, password: str):
            """Initializes the `Authentication` object.

            Generates a random salt, then hash the salted password with `hashlib.scrypt`.
            """

            # It is advised to generate salt of the same length as the resulting hash, i.e. 64 bytes.
            self.salt = bytes(os.urandom(64))  # TODO: needs to be unique
            self.hash = hashlib.scrypt(  # TODO: needs to be unique
                bytes(password, "utf-8"),
                salt=self.salt,
                n=self.n,
                r=self.r,
                p=self.p
            )

        @staticmethod
        def slow_equals(b1: bytes, b2: bytes) -> bool:
            """Compares two `bytes` objects.

            This comparision is done in a way that takes the same amount of time,
            regardless of how much of the bytes match.
            """

            diff = len(b1) ^ len(b2)
            for i in range(min(len(b1), len(b2))):
                diff = diff or b1[i] ^ b2[i]
            return diff == 0

        def authenticate(self, password: str) -> bool:
            """Check whether the given password is correct."""

            other_hash = hashlib.scrypt(
                bytes(password, "utf-8"),
                salt=self.salt,
                n=self.n,
                r=self.r,
                p=self.p
            )
            return self.slow_equals(self.hash, other_hash)

"""
class Comment:
    pass
"""


if __name__ == "__main__":
    print("Welcome to Cooking Bad!")
    print("Please create a new account.")
    name = input("Please enter your name: ")
    email = input("Please enter your email: ")
    password = getpass.getpass("Please choose a password: ")
    acc = Account(name, email, password)

    print("Please create a new recipe.")
    name = input("Please enter the name of the recipe: ")

    ingredients = list()
    while True:
        name = input("Please enter the name of the ingredient: ")
        amount = int(input("Please enter the amount of the ingredient: "))
        unit = input("Please enter the unit of the amount of the ingredient: ")
        ingredients.append(Ingredient(name, amount, unit))
        another = input("Do you wish to stop adding ingredients? [Y/n] ")
        if another == "Y":
            break

    portions = int(input("For how many portions are the ingredients? "))
    ingredient_list = IngredientList(portions, ingredients)

    instructions = list()
    while True:
        text = input("Please enter an instruction: ")
        instructions.append(Instruction(text))
        another = input("Do you wish to stop adding instructions? [Y/n] ")
        if another == "Y":
            break

    recipe = Recipe(name, ingredient_list, instructions)

    print("This is your recipe:")
    print(recipe)
    print("This recipe will now be added to your account.")

    acc.add_recipe(recipe)
