from crawler import discover_book_urls
from extractor import extract_book

if __name__ == "__main__":
    book_urls, pages_visited = discover_book_urls()
    print(f"catalogue_pages={pages_visited}")
    print(f"discovered={len(book_urls)}")
    print(f"unique_urls={len(set(u for u, _ in book_urls))}")

    records = []
    for i, (url, source_page) in enumerate(book_urls, start=1):
        cache_name = f"book-{i:03d}.html"
        record = extract_book(
            product_url=url,
            source_page=source_page,
            cache_name=cache_name,
        )
        records.append(record)

    print(f"detail_pages={len(records)}")
    print(records[0])