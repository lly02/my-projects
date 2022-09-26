import tkinter as tk
import tkinter.font as font
import re
import copy


class NutritionCardController(object):
    """
    Controller class for nutrition card.
    """
    def __init__(self, food):
        self.gui = NutritionCardGui()
        self.model = NutritionCardModel(food)

        self.gui.winfo_toplevel().title(self.model.food.brand_name)
        self.gui.option_measurement_input.set(
            self.model.serving_size_to_str(self.model.food.default_serving_size)
        )
        self.add_measurement_options(self.model.measurement_options)

        self.gui.ent_measurement_input.set(
            self.model.food.default_serving_size["value"]
        )
        self.gui.ent_measurement_input.trace_add("write", self.measurement_change)
        self.display_nutrition()

    def display_nutrition(self, *args):
        """
        Display the nutritional contents on the text widget.

        :param args: Get the KeyEvent when something is pressed which calls this method
        :type args: list, optional
        """
        self.gui.txt_main["state"] = "normal"
        self.gui.txt_main.delete("1.0", tk.END)
        self.gui.txt_main.insert(
            tk.END,
            f"{self.model.get_nutrition_display()}"
        )
        self.gui.txt_main["state"] = "disabled"

    def add_measurement_options(self, options):
        self.gui.option_measurement["menu"].delete(0, "end")

        for option in options:
            self.gui.option_measurement["menu"].add_command(
                label=option,
                command=tk._setit(self.gui.option_measurement_input, option, self.option_measurement_select)
            )

    def option_measurement_select(self, event):
        """
        A method to calculate the nutritional contents when the serving size is changed.

        :param event: The string passed in when the serving size is changed
        :type event: string
        """
        current_serving = self.gui.option_measurement_input.get()
        value, unit = self.model.get_value_unit_from_serving_str(current_serving)
        self.gui.ent_measurement_input.set(str(value))
        self.model.current_serving_size = self.model.find_current_serving(value, unit[1:])
        self.model.current_nutrition = self.model.find_current_nutrition(self.gui.ent_measurement_input.get())
        self.display_nutrition()

    def measurement_change(self, *args):
        """
        A method to calculate the nutritional contents when the measurement value is changed.

        :param args: Arguments by trace add
        :type args: string
        """
        if self.gui.ent_measurement_input.get() == "":
            self.gui.ent_measurement_input.set("0")
        if self.gui.ent_measurement_input.get()[-1].isdigit():
            self.model.current_nutrition = self.model.find_current_nutrition(self.gui.ent_measurement_input.get())
            self.display_nutrition()
        else:
            self.gui.ent_measurement_input.set(self.gui.ent_measurement_input.get()[:-1])


class NutritionCardModel(object):
    def __init__(self, food):
        self.food = food
        self.current_serving_size = copy.deepcopy(self.food.default_serving_size)
        self.current_nutrition = copy.deepcopy(self.food.default_nutrition)
        self.measurement_options = self.get_measurement_options()

    def get_measurement_options(self):
        return [str(serving_size["value"]) + " " + serving_size["unit"] for serving_size in self.food.serving_sizes]

    def process_content(self):
        """
        Process the nutrition contents to make it easier to display on the nutrition card.
            - Remove "_" and capitalize first word
            - Format the energy from { "Energy": { "Unit": "Calories", "Value": 100 } } to { "Energy": 100 Calories }
        :return: The formatted nutrition content
        :rtype: list
        """
        result = []
        for key, value in self.food.nutrition_contents.items():
            if isinstance(value, (str, int, float)):
                key = self.split_and_capitalize(key)
                result.append({key: str(value) + "g"})
            elif isinstance(value, dict):
                energy_unit = ""
                energy_value = ""
                for value_key, value_value in value.items():
                    if value_key == "unit":
                        energy_unit = value_value
                    elif value_key == "value":
                        energy_value = value_value
                result.append({self.split_and_capitalize(key): str(energy_value) + energy_unit})
            else:
                print(f"{value} not a string, integer or dictionary")
        return result

    def find_current_serving(self, value, unit):
        for serving in self.food.serving_sizes:
            if serving["value"] == value and serving["unit"] == unit:
                return serving

    def find_current_nutrition(self, energy_value):
        default_serving = self.food.default_serving_size
        result = copy.deepcopy(self.food.default_nutrition)
        for key, value in self.food.default_nutrition.items():
            if key == "energy":
                result[key]["value"] = round(float(value["value"]) / float(default_serving["value"])
                                             / float(default_serving["nutrition_multiplier"]) * float(energy_value)
                                             * float(self.current_serving_size["nutrition_multiplier"]), 2)
            else:
                result[key] = round(float(value) / float(default_serving["value"])
                                    / float(default_serving["nutrition_multiplier"]) * float(energy_value)
                                    * float(self.current_serving_size["nutrition_multiplier"]), 2)
        return result

    def get_nutrition_display(self):
        nutrition_display = ""
        for key, value in self.current_nutrition.items():
            if key == "energy":
                nutrition_display += f"Energy : {str(value['value'])} {self.split_and_capitalize(value['unit'])}\n"
            else:
                nutrition_display += f"{self.split_and_capitalize(key)} : {str(value)} g\n"
        return f"Brand Name: {self.food.brand_name}\n" \
               f"Description: {self.food.description}\n" \
               f"{nutrition_display}"

    @staticmethod
    def serving_size_to_str(serving):
        return str(serving["value"]) + " " + serving["unit"]

    @staticmethod
    def get_value_from_serving_size_str(serving):
        return serving.rstrip("abcdefghijklmnopqrstuvwxyz")

    @staticmethod
    def get_value_unit_from_serving_str(serving):
        """
        Split value, unit from serving size string E.g. 5grams to [5, grams].

        :param serving: The serving size string
        :return: Split value, unit
        :type: list
        """
        value = ""
        for count, letter in enumerate(serving):
            if letter.isdigit():
                value += letter
            else:
                break
        unit = serving[len(value):]

        return int(value), unit

    @staticmethod
    def split_and_capitalize(content):
        """
        To remove the "_" and capitalize the string

        :param content: The string that needs formatting
        :return: The formatted string
        :type: str
        """
        content = re.sub("_", " ", content).split(" ")
        content = " ".join([word.capitalize() for word in content])
        return content


class NutritionCardGui(tk.Tk):
    """
    A class that extends :class: `tkinter` to create the UI for the nutrition card.
    """
    def __init__(self):
        super().__init__()

        # Card frame
        self.geometry("400x600")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.defaultFont = "Calibri 15"

        # Main frame
        self.frm_main = tk.Frame(self)
        self.frm_main.grid(row=0, column=0, sticky="nsew")
        self.frm_main.columnconfigure(0, weight=1)
        self.frm_main.rowconfigure(0, weight=1)

        # Main text box
        self.txt_main = tk.Text(self.frm_main, font=self.defaultFont, wrap=tk.NONE)

        # Scrollbar for text box
        self.scroll_y = tk.Scrollbar(self.frm_main, orient=tk.VERTICAL, command=self.txt_main.yview)
        self.scroll_x = tk.Scrollbar(self.frm_main, orient=tk.HORIZONTAL, command=self.txt_main.xview)
        self.scroll_y.grid(row=0, column=1, stick="ns")
        self.scroll_x.grid(row=1, column=0, stick="ew")

        self.txt_main.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.txt_main.grid(row=0, column=0, sticky="nsew")

        # Selection frame
        self.frm_selection = tk.Frame(self, background="gray")
        self.frm_selection.grid(row=1, column=0, sticky="nsew")
        self.frm_selection.columnconfigure(1, weight=1)

        # Measurement value entry
        self.ent_measurement_input = tk.StringVar(self.frm_selection)
        self.ent_measurement = tk.Entry(self.frm_selection, font=self.defaultFont,
                                        textvariable=self.ent_measurement_input, width=3)
        self.ent_measurement.grid(row=0, column=0, padx=5, ipadx=5, ipady=5, sticky="w")

        # Serving size unit selection option menu
        self.option_measurement_input = tk.StringVar(self.frm_selection)
        self.option_measurement_options = [None]
        self.option_measurement = tk.OptionMenu(
            self.frm_selection,
            self.option_measurement_input,
            *self.option_measurement_options
        )
        self.option_measurement.config(font=font.Font(family="Calibri", size=50), width=5, anchor="w")
        self.option_measurement.grid(row=0, column=1, stick="ew")

        # Add to list button
        self.btn_add = tk.Button(self.frm_selection, font=self.defaultFont, text="Add")
        self.btn_add.grid(row=0, column=2, pady=5, padx=5, sticky="e")
