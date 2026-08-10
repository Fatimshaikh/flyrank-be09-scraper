from crawler import discover_book_urls
from extractor import extract_book
from schema import normalize_and_validate
from storage import save_books, save_errors

if __name__ == "__main__":
    book_urls, pages_visited = discover_book_urls()
    print(f"catalogue_pages={pages_visited}")
    print(f"discovered={len(book_urls)}")
    print(f"unique_urls={len(set(u for u, _ in book_urls))}")

    raw_records = []
    for i, (url, source_page) in enumerate(book_urls, start=1):
        cache_name = f"book-{i:03d}.html"
        record = extract_book(
            product_url=url,
            source_page=source_page,
            cache_name=cache_name,
        )
        raw_records.append(record)

    print(f"detail_pages={len(raw_records)}")

    # dedupe by canonical URL (product_url), keep first occurrence
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

    print(f"valid_records={len(valid_books)}")
    print(f"invalid_records={len(invalid_records)}")