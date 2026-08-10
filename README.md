# FlyRank BE-09 — The polite scraper

## Target classification
- **Site:** books.toscrape.com
- **Why it's appropriate:** Books to Scrape describes itself as a fictional
  bookstore built specifically to be scraped — a sandbox for people learning
  web scraping and developers testing scraping tools. It contains 1000 items,
  requires no JavaScript, and explicitly invites this kind of practice.
- **Scope:** the first 3 catalogue pages only (60 books total).
- **Data collected:** title, product URL, price, availability, star rating,
  description — all publicly listed on each book's own page.
- **robots.txt check:** requested `https://books.toscrape.com/robots.txt` on
  [date] — received a 404. No robots file exists. This is not itself
  permission; the actual justification is the site's own stated purpose above.

I will not reuse this code on another site without checking its rules and
terms first.

## How to run

\`\`\`bash
git clone https://github.com/Fatimshaikh/flyrank-be09-scraper.git
cd flyrank-be09-scraper
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash
pip install -r requirements.txt
python src/main.py
\`\`\`

Produces \`output/books.json\`, \`output/errors.json\`, and \`output/run-report.json\`.

## Stack
Python 3 + \`requests\` + BeautifulSoup + Pydantic.

## Record schema
| Field | Type | Notes |
|---|---|---|
| title | string | |
| product_url | string (URL) | canonical identity for dedup |
| price_gbp | float | parsed from price_text |
| price_text | string | original, kept alongside |
| availability_text | string | |
| rating | int (1–5) | parsed from star-rating word |
| description | string or null | some books have none |
| source_page | string | which catalogue page this book was discovered on |
| fetched_at | string (ISO datetime) | provenance timestamp |

## Politeness rules
- Identifying User-Agent: \`FlyRankInternshipA9/1.0 (+repo link)\`
- 10s timeout per request
- 0.6s delay between real requests (cache hits skip the delay)
- Status code checked before parsing; only 200 is treated as success
- One retry on timeout/5xx; no retry on 404/403
- Development reads from \`cache/\` instead of re-hitting the site

## Why no browser was needed
All the data (title, price, description, etc.) is present directly in the HTML
the server returns — confirmed by viewing page source before writing any
selector code. A headless browser would only add startup cost and complexity
with no benefit here, since nothing on Books to Scrape is rendered by
JavaScript after the initial page load.

## Sample run report
```json
{
  "started_at": "2026-08-10T18:54:50.553774+00:00",
  "duration_seconds": 1.43,
  "catalogue_pages_fetched": 3,
  "book_pages_attempted": 61,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1,
  "failed_page_details": [
    {
      "url": "https://books.toscrape.com/catalogue/this-book-does-not-exist_9999/index.html",
      "reason": "404 Client Error: Not Found for url: https://books.toscrape.com/catalogue/this-book-does-not-exist_9999/index.html"
    }
  ]
}
```

## Known limitation
One deliberately broken/fake book URL is included in every run to prove the
failure-handling path works end to end — this is why \`failed_pages\` is
always 1 in the committed \`run-report.json\`, and \`book_pages_attempted\`
is 61 rather than 60.

## Ethics note
This scraper only touches books.toscrape.com, a sandbox explicitly built and
intended for scraping practice. It would not be reused against a real site
without first checking that site's robots.txt and terms of service. Where an
official API exists, that should always be preferred over scraping. This
scraper collects only the fields needed for the assignment and does not
attempt to bypass any login, paywall, or access restriction.

## AI disclosure
Used Claude for guidance and code structure across all 6 stages, including
debugging (cache path resolution, encoding mojibake, source_page tracking).
Ran, tested, and understood every stage myself.