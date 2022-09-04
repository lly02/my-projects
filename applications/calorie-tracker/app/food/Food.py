from . import NutritionCard


class Food(object):
    def __init__(self, brand_name, description, nutrition_contents, serving_sizes):
        self.brand_name = brand_name
        self.description = description
        self.nutrition_contents = nutrition_contents
        self.serving_sizes = serving_sizes
        self.base_serving_sizes = [serving_size for serving_size in self.serving_sizes
                                   if str(serving_size["value"]).startswith("1")]
        self.nutrition_card = None

    # get serving size in grams if exists, else index 0 of self.serving_sizes
    def get_serving_size(self):
        result = None
        energy = self.nutrition_contents["energy"]["value"]
        serving = [serving for serving in self.serving_sizes
                   if serving["unit"] == "gram" and serving["value"] != 1]

        if len(serving) != 1:
            if len(serving) == 0:
                result = self.serving_sizes[0]
            if len(serving) > 1:
                match_value = min(serving, key=lambda x: abs(x['nutrition_multiplier'] - 1))['nutrition_multiplier']
                for serve in serving:
                    if serve["nutrition_multiplier"] == match_value:
                        result = serve
                        break
        else:
            result = serving[0]

        energy = energy * result["nutrition_multiplier"]

        return energy, result

    def create_nutrition_card(self):
        if self.nutrition_card is None:
            self.nutrition_card = NutritionCard.NutritionCard(self)
            self.nutrition_card.protocol("WM_DELETE_WINDOW",
                                         lambda: self.destroy_nutrition_card())
            self.nutrition_card.focus_force()
            self.nutrition_card.mainloop()
        else:
            self.nutrition_card.focus_force()

    def destroy_nutrition_card(self):
        if self.nutrition_card is not None:
            self.nutrition_card.destroy()
            self.nutrition_card = None
