import requests
from model import Product
from urllib.parse import quote

def scrape_ebay(keyword, limit=20):

    url = f"https://www.ebay.com/sch/i.html?_nkw={quote(keyword)}"

    try:
        html = requests.get(url, timeout=10).text
    except:
        return []

    return [
        Product(
            title=f"eBay results: {keyword}",
            price=None,
            url=url,
            image=None,
            source="ebay"
        )
    ]
