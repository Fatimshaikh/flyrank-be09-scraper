import os
import time
import requests

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/Fatimshaikh/flyrank-be09-scraper)"
TIMEOUT = 10  # seconds
DELAY = 0.6   # seconds, polite gap between real requests
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache")

os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(cache_name: str) -> str:
    return os.path.join(CACHE_DIR, cache_name)


def fetch(url: str, cache_name: str) -> str:
    """
    Fetch a URL politely, using a local cache during development.
    Returns the HTML text, or raises requests.HTTPError on a bad status.
    """
    path = _cache_path(cache_name)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"CACHE HIT  {url}  ({len(html)} bytes)")
        return html

    headers = {"User-Agent": USER_AGENT}
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()

    response.encoding = "utf-8"  # force correct decoding, avoid mojibake like 'Â£'
    html = response.text

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"FETCH      {url}  ({len(html)} bytes)")
    time.sleep(DELAY)  # only real requests wait — cache hits don't
    return html