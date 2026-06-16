from scraper_shopee import scrape_shopee
from scraper_mercari import scrape_mercari
from scraper_ebay import scrape_ebay
from scraper_yahoo import scrape_yahoo


def normalize(r):

    # dict already
    if isinstance(r, dict):
        return r

    # object (Product class)
    return {
        "title": getattr(r, "title", None),
        "price": getattr(r, "price", None),
        "url": getattr(r, "url", None),
        "image": getattr(r, "image", None),
        "source": getattr(r, "source", None),
    }


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

    return [normalize(r) for r in results]
