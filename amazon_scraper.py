from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random
from data_model import Product
from query_reader import read_queries
from data_saver import save_to_json

class AmazonScraper:
    BASE_URL = "https://www.amazon.com/s"

    def __init__(self, driver_path: str):
        self.driver_path = driver_path
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        """Initialize Selenium WebDriver."""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(self.driver_path)
        return webdriver.Chrome(service=service, options=options)

    def fetch_page(self, query: str, page: int) -> str:
        """Fetches the HTML of a search result page."""
        url = f"{self.BASE_URL}?k={query}&page={page}"
        try:
            print(f"Fetching URL: {url}")
            self.driver.get(url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".s-main-slot"))
            )
            return self.driver.page_source
        except Exception as e:
            print(f"Error fetching page {page} for query '{query}': {e}")
            return ""

    def parse_page(self, html: str) -> list:
        """Parses product details from a search result page."""
        soup = BeautifulSoup(html, "html.parser")
        product_elements = soup.select(".s-main-slot .s-result-item")

        products = []
        for product in product_elements:
            try:
                title = product.select_one("h2 a span").get_text(strip=True)
                total_reviews = product.select_one(".a-size-small .a-link-normal").get_text(strip=True)
                price = product.select_one(".a-price .a-offscreen").get_text(strip=True)
                image_url = product.select_one(".s-image")["src"]

                products.append(Product(
                    title=title,
                    total_reviews=total_reviews,
                    price=price,
                    image_url=image_url
                ).__dict__)
            except AttributeError:
                continue

        return products

    def scrape(self, query: str, max_pages: int = 20) -> list:
        """Scrapes products for a search query."""
        all_products = []
        for page in range(1, max_pages + 1):
            print(f"Scraping page {page} for query '{query}'...")
            time.sleep(random.uniform(2, 5))  
            html = self.fetch_page(query, page)
            if not html:
                break
            products = self.parse_page(html)
            all_products.extend(products)
        return all_products

    def close_driver(self):
        """Closes the Selenium WebDriver."""
        self.driver.quit()

if __name__ == "__main__":
    DRIVER_PATH = "chromedriver.exe"
    QUERIES_FILE = "user_queries.json"

    scraper = AmazonScraper(driver_path=DRIVER_PATH)
    try:
        queries = read_queries(QUERIES_FILE)
        for query in queries:
            print(f"Processing query: {query}")
            products = scraper.scrape(query, max_pages=20)
            save_to_json(products, f"{query}.json")
    finally:
        scraper.close_driver()
