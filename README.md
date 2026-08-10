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