from scraper import scrape_yahoo, scrape_shopee, scrape_ebay, scrape_mercari

def search_all(keyword, sources):

    results = []

    if "yahoo" in sources:
        results += scrape_yahoo(keyword)

    if "shopee" in sources:
        results += scrape_shopee(keyword)

    if "ebay" in sources:
        results += scrape_ebay(keyword)

    if "mercari" in sources:
        results += scrape_mercari(keyword)

    return results
