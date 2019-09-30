

# calculate daily macros
def macro_calculator(calories):
    carbs = int((0.40 * calories) / 4)
    proteins = int((0.35 * calories) / 4)
    fats = int((0.25 * calories) / 9)
    macros = {
        "carbs": carbs,
        "proteins": proteins,
        "fats": fats
    }
    return macros


def mealplan_calculator(calories, meal):
    calorie_index = calories / 1000

    for food in meal:
        meal[food] *= calorie_index
        meal[food] = int(round(meal[food]))
    return meal


class Food:

    # name and macros for 100g of food
    def __init__(self, name, carbs, proteins, fats):
        self.fats = fats
        self.proteins = proteins
        self.carbs = carbs
        self.name = name


# from nutritionix.com
chicken_breast = Food(name="chicken breast", carbs=0, proteins=31, fats=3.6)
white_rice = Food(name="white rice", carbs=28, proteins=2.7, fats=0.3)