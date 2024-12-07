from dataclasses import dataclass
from datetime import datetime

@dataclass
class Product:
    title: str
    total_reviews: str
    price: str
    image_url: str
    scrape_date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
