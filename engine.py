from scraper_shopee import scrape_shopee
from scraper_mercari import scrape_mercari
from scraper_ebay import scrape_ebay
from scraper_yahoo import scrape_yahoo


def search_all(keyword, sources):

    results = []

    mapping = {
        "shopee": scrape_shopee,
        "mercari": scrape_mercari,
        "ebay": scrape_ebay,
        "yahoo": scrape_yahoo,
    }

    for s in sources:
        try:
            results += mapping[s](keyword)
        except:
            continue

    # remove empty titles
    def safe_dict(r):

    if not isinstance(r, dict):
        return None

    if not r.get("title"):
        return None

    return r


def search_all(keyword, sources):

    results = []

    if "shopee" in sources:
        results += scrape_shopee(keyword)

    if "mercari" in sources:
        results += scrape_mercari(keyword)

    if "ebay" in sources:
        results += scrape_ebay(keyword)

    if "yahoo" in sources:
        results += scrape_yahoo(keyword)

    cleaned = []

    for r in results:
        r2 = safe_dict(r)
        if r2:
            cleaned.append(r2)

    return cleaned
