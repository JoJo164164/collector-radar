from scraper_shopee import scrape_shopee
from scraper_mercari import scrape_mercari
from scraper_ebay import scrape_ebay
from scraper_yahoo import scrape_yahoo

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

    return results
