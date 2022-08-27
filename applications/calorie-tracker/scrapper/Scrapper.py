import threading
import requests
import concurrent.futures


class Scrapper(object):
    api_url = "https://www.myfitnesspal.com/api/nutrition?"

    def __init__(self):
        self.result = []
        self.lock = threading.Lock()

    def search(self, query):
        self.result = []
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

        result_arr = r.json()["items"]

        # extract the needed information
        for item in result_arr:
            food = item["item"]

            try:
                food.get("brand_name")
            except KeyError:
                food["brand_name"] = None

            with self.lock:
                self.result.extend([(
                    {
                        "brand_name": food.get("brand_name", None),
                        "description": food.get("description", None),
                        "nutritional_contents": food.get("nutritional_contents", None),
                        "serving_sizes": food.get("serving_sizes", None)
                    }
                )])