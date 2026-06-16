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
    return [r for r in results if r.get("title")]
