from fetcher import fetch

if __name__ == "__main__":
    html = fetch(
        "https://books.toscrape.com/catalogue/page-1.html",
        "catalogue-page-1.html",
    )
    print("Done. Length:", len(html))