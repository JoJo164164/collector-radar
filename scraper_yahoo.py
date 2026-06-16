import requests
from model import Product
from urllib.parse import quote

def scrape_yahoo(keyword):

    url = f"https://tw.search.yahoo.com/search?p={quote(keyword)}"

    try:
        requests.get(url, timeout=10)
    except:
        pass

    return [
        Product(
            title=f"Yahoo search: {keyword}",
            price=None,
            url=url,
            image=None,
            source="yahoo"
        )
    ]
