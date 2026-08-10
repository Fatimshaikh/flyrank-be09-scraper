import time
from datetime import datetime, timezone

from crawler import discover_book_urls
from extractor import extract_book
from schema import normalize_and_validate
from storage import save_books, save_errors, save_report

# one deliberately fake URL to prove failure handling — remove before final submission
# or keep permanently and just note it in the README, your call
FAKE_BOOK_URL = "https://books.toscrape.com/catalogue/this-book-does-not-exist_9999/index.html"

if __name__ == "__main__":
    start_time = time.time()
    started_at = datetime.now(timezone.utc).isoformat()

    book_urls, pages_visited = discover_book_urls()
    print(f"catalogue_pages={pages_visited}")
    print(f"discovered={len(book_urls)}")
    print(f"unique_urls={len(set(u for u, _ in book_urls))}")

    # inject the fake URL to prove Stage 5 works — comment out to run "clean"
    book_urls = book_urls + [(FAKE_BOOK_URL, "https://books.toscrape.com/catalogue/page-1.html")]

    raw_records = []
    failed_pages = []
    cache_hits = 0
    fetches = 0

    for i, (url, source_page) in enumerate(book_urls, start=1):
        cache_name = f"book-{i:03d}.html"
        try:
            record = extract_book(product_url=url, source_page=source_page, cache_name=cache_name)
            raw_records.append(record)
        except Exception as e:
            print(f"FAILED     {url}  ({e})")
            failed_pages.append({"url": url, "reason": str(e)})

    print(f"detail_pages={len(raw_records)}")

    seen_urls = set()
    valid_books = []
    invalid_records = []

    for raw in raw_records:
        url = raw["product_url"]
        if url in seen_urls:
            continue
        seen_urls.add(url)

        try:
            book = normalize_and_validate(raw)
            valid_books.append(book.model_dump(mode="json"))
        except Exception as e:
            invalid_records.append({"raw": raw, "reason": str(e)})

    save_books(valid_books)
    save_errors(invalid_records)

    duration_seconds = round(time.time() - start_time, 2)

    report = {
        "started_at": started_at,
        "duration_seconds": duration_seconds,
        "catalogue_pages_fetched": pages_visited,
        "book_pages_attempted": len(book_urls),
        "valid_records": len(valid_books),
        "invalid_records": len(invalid_records),
        "failed_pages": len(failed_pages),
        "failed_page_details": failed_pages,
    }
    save_report(report)

    print(f"valid_records={len(valid_books)}")
    print(f"invalid_records={len(invalid_records)}")
    print(f"failed_pages={len(failed_pages)}")