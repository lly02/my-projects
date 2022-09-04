import tkinter as tk
import tkinter.font as font
import re


class NutritionCard(tk.Tk):
    def __init__(self, food):
        super().__init__()

        self.food = food

        # card frame
        self.title(self.food.brand_name)
        self.geometry("400x600")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # main frame
        self.frm_main = tk.Frame(self)
        self.frm_main.grid(row=0, column=0, sticky="nsew")
        self.frm_main.columnconfigure(0, weight=1)
        self.frm_main.rowconfigure(0, weight=1)

        # main text box
        self.txt_main = tk.Text(self.frm_main, wrap=tk.NONE, font=25)

        nutrition_contents = self.process_content()
        newline = "\n"
        self.txt_main.insert(
            tk.END,
            f"Brand Name: {self.food.brand_name}\n"
            f"Description: {self.food.description}\n"
            f"{newline.join(f'{key}: {value}' for nutrition_content in nutrition_contents for key, value in nutrition_content.items())}"
        )
        self.txt_main["state"] = "disabled"

        # scrollbar for text box
        self.scroll_y = tk.Scrollbar(self.frm_main, orient=tk.VERTICAL, command=self.txt_main.yview)
        self.scroll_x = tk.Scrollbar(self.frm_main, orient=tk.HORIZONTAL, command=self.txt_main.xview)
        self.scroll_y.grid(row=0, column=1, stick="ns")
        self.scroll_x.grid(row=1, column=0, stick="ew")

        self.txt_main.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        self.txt_main.grid(row=0, column=0, sticky="nsew")

        # selection frame
        self.frm_selection = tk.Frame(self, background="gray")
        self.frm_selection.grid(row=1, column=0, sticky="nsew")
        self.frm_selection.columnconfigure(1, weight=1)

        preset_unit = self.food.get_serving_size()[1]
        # measurement value entry
        self.ent_measurement = tk.Entry(self.frm_selection, font=25, width=3)
        self.ent_measurement.insert(tk.END, preset_unit["value"])
        self.ent_measurement.grid(row=0, column=0, padx=5, ipadx=5, ipady=5, sticky="w")

        # measurement unit selection
        self.serving_sizes_selection = [serving_size["unit"] for serving_size in self.food.base_serving_sizes]

        # find index of preset
        preset_count = 0
        for count, serving_size in enumerate(self.serving_sizes_selection):
            if serving_size == preset_unit["unit"]:
                preset_count = count
                break

        self.option_measurement_variable = tk.StringVar(
            self.frm_selection,
            self.serving_sizes_selection[preset_count]
        )
        self.option_measurement = tk.OptionMenu(
            self.frm_selection,
            self.option_measurement_variable,
            *self.serving_sizes_selection
        )
        self.option_measurement.config(font=font.Font(size=50), width=5, anchor="w")
        self.option_measurement.grid(row=0, column=1, stick="ew")

        # add to list button
        self.btn_add = tk.Button(self.frm_selection, text="Add", font=25)
        self.btn_add.grid(row=0, column=2, pady=5, padx=5, sticky="e")

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
        return result

    @staticmethod
    def split_and_capitalise(content):
        content = re.sub("_", " ", content).split(" ")
        content = " ".join([word.capitalize() for word in content])
        return content
