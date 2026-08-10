import re
from typing import Optional
from pydantic import BaseModel, HttpUrl, field_validator

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class Book(BaseModel):
    title: str
    product_url: HttpUrl
    price_gbp: float
    price_text: str
    availability_text: str
    rating: int
    description: Optional[str] = None
    source_page: str
    fetched_at: str

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("title is empty")
        return v


def clean_price(price_text: str) -> float:
    """'£51.77' -> 51.77"""
    match = re.search(r"[\d.]+", price_text)
    if not match:
        raise ValueError(f"could not parse price from {price_text!r}")
    return float(match.group())


def clean_rating(rating_text: str) -> int:
    """'Three' -> 3"""
    if rating_text not in RATING_MAP:
        raise ValueError(f"unknown rating word {rating_text!r}")
    return RATING_MAP[rating_text]


def normalize_and_validate(raw: dict) -> Book:
    """
    Take one raw record from the extractor and turn it into a
    validated Book. Raises ValueError/pydantic.ValidationError on
    bad data — caller decides what to do with the failure.
    """
    return Book(
        title=raw["title"],
        product_url=raw["product_url"],
        price_gbp=clean_price(raw["price_text"]),
        price_text=raw["price_text"],
        availability_text=raw["availability_text"],
        rating=clean_rating(raw["rating_text"]),
        description=raw["description"],
        source_page=raw["source_page"],
        fetched_at=raw["fetched_at"],
    )