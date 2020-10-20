# datenbanken etc.
# website/gui etc.

class Account:
    # password: salted hash (hashlib)
    pass

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

class Instruction:
    pass

class Comment:
    pass


if __name__ == "__main__":
    a = Account()
    i = Ingredient("Lauchzwiebel", 1)
    il = IngredientList(1, [i])
    r = Recipe(a, il)
    print(r)
    
