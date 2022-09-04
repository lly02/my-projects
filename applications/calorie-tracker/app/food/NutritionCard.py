import tkinter as tk
import re


class NutritionCard(tk.Tk):
    def __init__(self, food):
        super().__init__()

        self.food = food

        # card frame
        self.title(self.food.brand_name)
        self.geometry("400x600")
        self.resizable(False, False)

        # main frame
        self.frm_main = tk.Frame(self)
        self.frm_main.pack()

        # main text box
        self.txt_main = tk.Text(self.frm_main, wrap=tk.NONE, font=25)

        self.process_content()
        newline = "\n"
        self.txt_main.insert(
            tk.END,
            f"{newline.join(f'{key}: {value}' for nutrition_content in self.food.nutrition_contents for key, value in nutrition_content.items())}"
        )
        self.txt_main["state"] = "disabled"

        # scrollbar for text box
        self.scroll_y = tk.Scrollbar(self.frm_main, orient=tk.VERTICAL, command=self.txt_main.yview)
        self.scroll_x = tk.Scrollbar(self.frm_main, orient=tk.HORIZONTAL, command=self.txt_main.xview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.txt_main.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        self.txt_main.pack()

    def process_content(self):
        result = []
        for key, value in self.food.nutrition_contents.items():
            if isinstance(value, (str, int, float)):
                key = self.split_and_capitalise(key)
                result.append({key: str(value) + "g"})
            elif isinstance(value, dict):
                energy_unit = ""
                energy_value = ""
                for value_key, value_value in value.items():
                    if value_key == "unit":
                        energy_unit = value_value
                    elif value_key == "value":
                        energy_value = value_value
                result.append({self.split_and_capitalise(key): str(energy_value) + energy_unit})
            else:
                print(f"{value} not a string, integer or dictionary")
        self.food.nutrition_contents = result

    @staticmethod
    def split_and_capitalise(content):
        content = re.sub("_", " ", content).split(" ")
        content = " ".join([word.capitalize() for word in content])
        return content
