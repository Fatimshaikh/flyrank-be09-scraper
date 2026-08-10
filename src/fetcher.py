import os
import time
import requests

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/Fatimshaikh/flyrank-be09-scraper)"
TIMEOUT = 10
DELAY = 0.6
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache")

os.makedirs(CACHE_DIR, exist_ok=True)


def _cache_path(cache_name: str) -> str:
    return os.path.join(CACHE_DIR, cache_name)


def fetch(url: str, cache_name: str) -> str:
    """
    Fetch a URL politely, using a local cache during development.
    Retries once on timeout or 5xx. Does NOT retry on 404/403.
    Raises requests.HTTPError or requests.RequestException on failure.
    """
    path = _cache_path(cache_name)

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"CACHE HIT  {url}  ({len(html)} bytes)")
        return html

    headers = {"User-Agent": USER_AGENT}
    attempts = 0
    max_attempts = 2  # one try + one retry

    while attempts < max_attempts:
        attempts += 1
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT)

            if response.status_code == 200:
                response.encoding = "utf-8"
                html = response.text
                with open(path, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"FETCH      {url}  ({len(html)} bytes)")
                time.sleep(DELAY)
                return html

            if response.status_code in (404, 403):
                # don't retry — asking again won't help
                response.raise_for_status()

            if response.status_code >= 500 and attempts < max_attempts:
                print(f"RETRY      {url}  (status {response.status_code})")
                time.sleep(1)
                continue

            response.raise_for_status()

        except requests.Timeout:
            if attempts < max_attempts:
                print(f"RETRY      {url}  (timeout)")
                time.sleep(1)
                continue
            raise

    raise requests.RequestException(f"failed to fetch {url} after {max_attempts} attempts")