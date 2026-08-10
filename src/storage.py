import json
import os

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output"
)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_books(books: list[dict], filename: str = "books.json"):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)


def save_errors(errors: list[dict], filename: str = "errors.json"):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(errors, f, indent=2, ensure_ascii=False)