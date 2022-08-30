import tkinter as tk
import math

from . import Scrapper


class Search(tk.Tk):
    def __init__(self):
        super().__init__()

        # main frame
        self.title("Calorie Tracker")
        self.geometry("800x600")
        self.resizable(False, False)

        # string var
        self.query = tk.StringVar()

        # header frame
        self.frm_header = tk.Frame(self, relief=tk.RAISED, borderwidth=5, bg="gray")
        self.frm_header.grid_columnconfigure(0, weight=1)
        self.frm_header.pack(fill=tk.X)

        # search bar
        self.ent_search = tk.Entry(self.frm_header, textvariable=self.query, font=25)
        self.ent_search.bind("<Return>", self.search)
        self.ent_search.grid(column=0, row=0, pady=10, padx=10, sticky="nsew")

        # enter button
        self.btn_enter = tk.Button(self.frm_header, text="Search", height=1, font=25, command=self.search)
        self.btn_enter.grid(column=1, row=0, pady=10, padx=10)

        # result frame
        self.frm_result = tk.Frame(self, relief=tk.RAISED, bg="gray")
        self.frm_result.pack(fill=tk.BOTH, expand=True)
        self.frm_result.columnconfigure(0, weight=1)

        # pagination bar
        self.frm_pagination = tk.Frame(self, bg="gray")
        self.frm_pagination.pack(fill=tk.BOTH)

        # pagination buttons wrap
        self.frm_pagination_button = tk.Frame(self.frm_pagination, bg="gray")
        self.frm_pagination_button.pack(ipady=15)

        # init Scrapper.py
        self.scrapper = Scrapper.Scrapper()

    def search(self, *args):
        # pattern = f"^.*{self.query.get()}.*$"
        # results = [x for x in db.data if re.fullmatch(pattern, x[0], re.IGNORECASE)]
        try:
            results = [result for result in self.scrapper.search(self.query.get()) if len(result) != 0]
        except TypeError:
            results = []

        if len(results) == 0:
            print("Nothing found!")
        else:
            self.display_results(results)

        self.query.set("")

    def display_results(self, results, page=1):
        # clear the results
        for widget in self.frm_result.winfo_children():
            widget.destroy()
        for widget in self.frm_pagination_button.winfo_children():
            widget.destroy()

        results_buttons = []

        for page_result in results:
            for result in page_result:
                energy, nutrition = result.get_serving_size()

                results_buttons.append(
                    tk.Button(
                        self.frm_result,
                        text=f"{result.brand_name} ({result.description})"
                             f"\n"
                             f"{energy}kcal / {nutrition['value']} {nutrition['unit']}",
                        justify=tk.LEFT,
                        anchor="nw",
                        borderwidth=5,
                        font=25
                    )
                )

        # insert result buttons into the result frame
        # try except for when len of last page is lesser than 5
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

        # pagination buttons (<, ..., >)
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
        # actual pagination numbers
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


if __name__ == "__main__":
    search = Search()
    search.mainloop()
