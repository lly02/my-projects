from . import nutrition_card


class Food(object):
    """
    A class to represent food.

    :param brand_name: The name of the food's brand ( Grilled chicken )
    :type brand_name: str
    :param description: A description of the food ( Chicken )
    :type description: str
    :param nutrition_contents: All the nutritional contents of the food ( { "calcium": 2, ... } )
    :type nutrition_contents: dict
    :param serving_sizes: The serving sizes available for the food ( [ { "id":1, "unit":"oz", "value":4 }, ... ] )
    :type serving_sizes: list
    """
    def __init__(self, brand_name, description, nutrition_contents, serving_sizes):
        self.brand_name = brand_name
        self.description = description
        self.nutrition_contents = nutrition_contents
        self.serving_sizes = serving_sizes
        self.nutrition_card = None
        self.default_serving_size = self.get_default_serving_size()
        self.default_nutrition = self.get_default_nutrition()

    def get_default_serving_size(self):
        """
        Get the serving size of the food in grams if it exists. Else get the first ( index 0 ) serving size.

        :return: Serving size information
        :rtype: dict
        """
        result = None
        grams_serving_size_index = self.get_serving_sizes_in_grams()
        if len(grams_serving_size_index) != 1:
            if len(grams_serving_size_index) == 0:
                result = self.serving_sizes[0]
            elif len(grams_serving_size_index) > 1:
                result = self.closest_to_multiplier_one(grams_serving_size_index)
        else:
            result = self.serving_sizes[grams_serving_size_index[0]]

        return result

    def get_default_nutrition(self):
        multiplier = self.default_serving_size["nutrition_multiplier"]
        nutrition = self.nutrition_contents.copy()
        for key, value in self.nutrition_contents.items():
            if key == "energy":
                nutrition[key]["value"] = round(self.nutrition_contents[key]["value"] * multiplier, 2)
            else:
                nutrition[key] = round(self.nutrition_contents[key] * multiplier, 2)
        return nutrition

    def get_serving_sizes_in_grams(self):
        """
        From serving sizes, find those index with serving size as grams.

        :return: List of indexes with unit as grams
        :rtype: list
        """
        result = []
        for count, serving_size in enumerate(self.serving_sizes):
            if serving_size["unit"] == "gram" and serving_size["value"] != 1:
                result.append(count)
        return result

    def closest_to_multiplier_one(self, serving_index):
        """
        Calculates the serving size nutrition multiplier that is closest to 1.

        :param serving_index: Indexes of the serving size to compare
        :type serving_index: list
        :return: Serving size information
        :rtype: dict
        """
        serving_sizes = [self.serving_sizes[index] for index in serving_index]
        return min(
            serving_sizes,
            key=lambda x: abs(x['nutrition_multiplier'] - 1)
        )

    def create_nutrition_card(self):
        """
        A method to create a nutrition card for the food item when its button is clicked.
        """
        if self.nutrition_card is None:
            self.nutrition_card = nutrition_card.NutritionCardController(self)
            self.nutrition_card.gui.protocol("WM_DELETE_WINDOW", self.destroy_nutrition_card)
            self.nutrition_card.gui.focus_force()
            self.nutrition_card.gui.mainloop()
        else:
            self.nutrition_card.gui.focus_force()

    def destroy_nutrition_card(self):
        """
        A method to destroy the nutrition card once the user adds the food or close the card.
        """
        if self.nutrition_card is not None:
            self.nutrition_card.gui.destroy()
            self.nutrition_card = None
