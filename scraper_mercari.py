import requests
from model import Product

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_mercari(keyword, limit=20):

    url = "https://www.mercari.com/us/api/v2/search"

    params = {
        "keyword": keyword,
        "page_size": limit
    }

    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        data = r.json()
    except:
        return []

    results = []

    items = data.get("items", [])

    for item in items:
        try:
            title = item.get("name")
            price = item.get("price")
            url = "https://www.mercari.com/us/item/" + item.get("id")
            image = item.get("photo_url")

            results.append(Product(
                title=title,
                price=str(price),
                url=url,
                image=image,
                source="mercari"
            ))

        except:
            continue

    return results
