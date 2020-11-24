# datenbanken etc.
# website/gui etc.
# TODO: testing
import os
import hashlib

class Account:
    # verlinkung zu social media
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.authentication = self.Authentication(password)

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

class Ingredient:
    # convert etc.
    def __init__(self, name: str, amount: int):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return f"{self.amount} {self.name}"

class IngredientList:
    def __init__(self, portions: int, ingredients: [Ingredient]):
        self.portions = portions
        self.ingredients = ingredients

class Recipe:
    def __init__(self, author: Account, ingredient_list: IngredientList):
        self.author = author
        self.ingredient_list = ingredient_list
# hallo henriman
class Instruction:
    pass

class Comment:
    pass


if __name__ == "__main__":
    a = Account("Henri", "henri.inndorf@gmail.com", "1234")
    """
    i = Ingredient("Lauchzwiebel", 1)
    il = IngredientList(1, [i])
    r = Recipe(a, il)
    print(r)
    """
    print(a.authentication.authenticate("1234"))
    print(a.authentication.authenticate("5678"))

