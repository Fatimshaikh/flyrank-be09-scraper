from crawler import discover_book_urls

if __name__ == "__main__":
    book_urls, pages_visited = discover_book_urls()
    print(f"catalogue_pages={pages_visited}")
    print(f"discovered={len(book_urls)}")
    print(f"unique_urls={len(set(book_urls))}")