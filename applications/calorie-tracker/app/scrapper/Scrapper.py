import threading
import requests
import concurrent.futures

from ..food import Food


class Scrapper(object):
    api_url = "https://www.myfitnesspal.com/api/nutrition?"

    def __init__(self):
        self.result = [None] * 10
        self.lock = threading.Lock()

    def search(self, query):
        self.result = [None] * 10
        #  using threads to search through 10 pages
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for x in range(1, 11):
                executor.submit(self.scrape, query, x)
        return self.result

    def scrape(self, query, page):
        url = f"{self.api_url}query={query}&page={page}"

        try:
            r = requests.get(url)
        except requests.exceptions.RequestException as e:
            SystemExit(e)

        results = r.json()["items"]

        # extract the needed information
        with self.lock:
            page_result = []

            for result in results:
                food = result["item"]

                try:
                    food.get("brand_name")
                except KeyError:
                    food["brand_name"] = "Generic"

                page_result.append(Food.Food(
                    food.get("brand_name"),
                    food.get("description"),
                    food.get("nutritional_contents"),
                    food.get("serving_sizes")
                ))

            self.result[page - 1] = page_result
