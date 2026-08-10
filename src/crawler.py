from urllib.parse import urljoin
from bs4 import BeautifulSoup

from fetcher import fetch

BASE_CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-1.html"
MAX_PAGES = 3


def discover_book_urls():
    """
    Walk the catalogue pages (following 'next' links) up to MAX_PAGES,
    collect every book's absolute URL. Returns (book_urls, pages_visited).
    """
    book_urls = []
    pages_visited = 0

    page_url = BASE_CATALOGUE_URL
    page_num = 1

    while page_url and pages_visited < MAX_PAGES:
        cache_name = f"catalogue-page-{page_num}.html"
        html = fetch(page_url, cache_name)
        pages_visited += 1

        soup = BeautifulSoup(html, "html.parser")

        for article in soup.select("article.product_pod h3 a"):
            href = article.get("href")
            absolute_url = urljoin(page_url, href)
            book_urls.append(absolute_url)

        if pages_visited < MAX_PAGES:
            next_link = soup.select_one("li.next a")
            if next_link:
                page_url = urljoin(page_url, next_link.get("href"))
                page_num += 1
            else:
                page_url = None
        else:
            page_url = None

    seen = set()
    unique_urls = []
    for url in book_urls:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)

    return unique_urls, pages_visited