from datetime import datetime, timezone
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from fetcher import fetch

RATING_WORDS = {"One", "Two", "Three", "Four", "Five"}


def extract_book(product_url: str, source_page: str, cache_name: str) -> dict:
    """
    Fetch one book's page and pull the 8 raw fields from it.
    Returns a dict — no cleaning/typing yet, that's Stage 4.
    """
    html = fetch(product_url, cache_name)
    soup = BeautifulSoup(html, "html.parser")

    product_area = soup.select_one("div.product_main")
    info_table = soup.select_one("table.table.table-striped")

    title = product_area.select_one("h1").get_text(strip=True)

    price_text = product_area.select_one("p.price_color").get_text(strip=True)

    availability_text = product_area.select_one(
        "p.instock.availability"
    ).get_text(strip=True)

    rating_classes = product_area.select_one("p.star-rating")["class"]
    rating_text = next(
        (cls for cls in rating_classes if cls in RATING_WORDS), None
    )

    description_tag = soup.select_one("#product_description ~ p")
    description = description_tag.get_text(strip=True) if description_tag else None

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }