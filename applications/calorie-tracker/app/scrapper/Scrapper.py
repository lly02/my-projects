import threading
import requests
import concurrent.futures

from ..food import food


class Scrapper(object):
    """
    A class to represent the web-scrapper.
    """
    api_url = "https://www.myfitnesspal.com/api/nutrition?"

    def __init__(self):
        self.result = [None] * 10
        self.lock = threading.Lock()

    def search(self, query):
        """
        To initialize the scrapper with threads. Then call the self scrape using threads to scrape results.

        :param query: The string which the scrapper will use to match the food item
        :type query: str
        :return: The scrapped result of Food object in [ [ { Food }, ... ], ... ]
        :rtype: list
        """
        # Reset the result everytime the method is called
        self.result = [None] * 10
        #  Use max of 10 threads to search through 10 pages
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            for x in range(1, 11):
                executor.submit(self.scrape, query, x)
        return self.result

    def scrape(self, query, page):
        """
        Scrape the user input for matching food item results in the website using threads.

        :param query: The string which the scrapper will use to match the food item
        :type query: str
        :param page: The page number to get the result from
        :type page: int
        :raises requests.exceptions.RequestException: Checks if the website is down
        :raises KeyError: Replace food["brand_name"] with "Generic" if it is None
        """
        url = f"{self.api_url}query={query}&page={page}"

        try:
            r = requests.get(url)
        except requests.exceptions.RequestException as e:
            SystemExit(e)

        results = r.json()["items"]

        # Lock the thread so that only one thread can change self.result at a time
        with self.lock:
            page_result = []

            for result in results:
                food_item = result["item"]

                try:
                    food_item.get("brand_name")
                except KeyError:
                    food_item["brand_name"] = "Generic"

                page_result.append(food.Food(               # Extends Food which creates a food object
                    food_item.get("brand_name"),            # Brand name ( Grilled chicken )
                    food_item.get("description"),           # Description ( Chicken )
                    food_item.get("nutritional_contents"),  # Nutritional contents ( { "calcium": 2, ... } )
                    food_item.get("serving_sizes")          # Serving sizes ( [ { "id":1, "unit":"oz", "value":4 }, ... ] )
                ))

            self.result[page - 1] = page_result
