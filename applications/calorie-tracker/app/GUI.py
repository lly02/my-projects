from .scrapper import search


class Gui(object):
    def __init__(self):
        self.search = search.Search()
        self.search.mainloop()
