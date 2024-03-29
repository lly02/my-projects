import tkinter as tk
import math

from . import scrapper


class Search(tk.Tk):
    """
    A class that extends :class:`tkinter` to create the Search UI which allows user to search for a food item.
    It retrieves data from the website https://www.myfitnesspal.com/.
    """

    def __init__(self):
        """
        Initialize tk and start generating the UI
        """
        super().__init__()

        # Main frame
        self.title("Calorie Tracker")
        self.geometry("800x600")
        self.resizable(False, False)
        self.defaultFont = "Calibri 15"

        # Header frame
        self.frm_header = tk.Frame(self, relief=tk.RAISED, borderwidth=5, bg="gray")
        self.frm_header.grid_columnconfigure(0, weight=1)
        self.frm_header.pack(fill=tk.X)

        # StringVar to retrieve data from user input in self.ent_search
        self.query = tk.StringVar()

        # Search bar
        self.ent_search = tk.Entry(self.frm_header, font=self.defaultFont, textvariable=self.query)
        self.ent_search.bind("<Return>", self.search)
        self.ent_search.grid(column=0, row=0, pady=10, padx=10, sticky="nsew")
        self.ent_search.focus_force()

        # Enter button
        self.btn_enter = tk.Button(self.frm_header, text="Search", height=1, font=self.defaultFont, command=self.search)
        self.btn_enter.grid(column=1, row=0, pady=10, padx=10)

        # Result frame
        self.frm_result = tk.Frame(self, relief=tk.RAISED, bg="gray")
        self.frm_result.pack(fill=tk.BOTH, expand=True)
        self.frm_result.columnconfigure(0, weight=1)

        # Pagination bar
        self.frm_pagination = tk.Frame(self, bg="gray")
        self.frm_pagination.pack(fill=tk.BOTH)

        # Pagination buttons wrap
        self.frm_pagination_button = tk.Frame(self.frm_pagination, bg="gray")
        self.frm_pagination_button.pack(ipady=15)

        # Init scrapper.py
        self.scrapper = scrapper.Scrapper()

    def search(self, *args):
        """
        Search the website https://www.myfitnesspal.com/ for the user input food item. Calls self.display_results to
        generate the result buttons.

        :param args: Receives the information about the KeyPress event when user searches
        :type args: tuple, optional
        :raises TypeError: If result is empty, set result as empty
        """
        try:
            results = [result for result in self.scrapper.search(self.query.get()) if len(result) != 0]
        except TypeError:
            results = []

        if len(results) == 0:
            print("Nothing found!")
        else:
            self.display_results(results)
        # Reset the entry field
        self.query.set("")

    def display_results(self, results, page=1):
        """
        Organise the results into buttons which are split into multiple pages

        :param results: A list of results from the scrapper to populate the buttons
        :type results: list
        :param page: Go to the page
        :type page: int, optional
        :raises IndexError: To stop inserting buttons on the last page if the number of buttons is less than 5
        """
        # Clear the buttons
        for widget in self.frm_result.winfo_children():
            widget.destroy()
        for widget in self.frm_pagination_button.winfo_children():
            widget.destroy()

        results_buttons = []

        for page_result in results:
            for result in page_result:
                serving = result.default_serving_size
                nutrition = result.default_nutrition

                results_buttons.append(
                    tk.Button(
                        self.frm_result,
                        text=f"{result.brand_name} ({result.description})"
                             f"\n"
                             f"{nutrition['energy']['value']}calories / {serving['value']} {serving['unit']}",
                        justify=tk.LEFT,
                        anchor="nw",
                        font=self.defaultFont,
                        borderwidth=5,
                        command=lambda current=result: current.create_nutrition_card()
                    )
                )

        # Try except for when len of last page is lesser than 5
        try:
            for count, x in enumerate(range((page - 1) * 5, page * 5)):
                results_buttons[x].grid(
                    row=count,
                    column=0,
                    sticky="ew",
                    padx=10,
                    pady=10
                )
        except IndexError:
            pass

        # Pagination buttons ( <, 1, 2, ... , > )
        btn_pagination = [
            tk.Button(
                self.frm_pagination_button,
                text="<",
                command=lambda: self.display_results(results, 1 if page - 1 == 0 else page - 1)
            ),
            tk.Button(
                self.frm_pagination_button, text=">",
                command=lambda: self.display_results(results,
                                                     page if page * 5 >= len(results_buttons) else page + 1)
            )
        ]
        # Insert the pagination numbers
        btn_pagination[1:1] = [
            tk.Button(
                self.frm_pagination_button,
                text=x,
                command=lambda k=x: self.display_results(results, k)
            )
            if x != page
            else tk.Button(
                self.frm_pagination_button,
                text=x,
                command=lambda k=x: self.display_results(results, k),
                bg="gray"
            )
            for x in range(1, math.ceil(len(results_buttons) / 5) + 1)
        ]

        for button in btn_pagination:
            button.pack(side=tk.LEFT)
