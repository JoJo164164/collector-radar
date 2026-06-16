import requests
from model import Product

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}


def scrape_shopee(keyword, limit=20):

    url = "https://shopee.tw/api/v4/search/search_items"

    params = {
        "by": "relevancy",
        "keyword": keyword,
        "limit": limit,
        "newest": 0,
        "order": "desc",
        "page_type": "search"
    }

    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        data = r.json()
    except:
        return []

    results = []

    items = data.get("items", [])

    for i in items:
        try:
            item = i.get("item_basic", {})

            title = item.get("name")
            price = item.get("price") / 100000
            image = "https://cf.shopee.tw/file/" + item.get("image", "")
            itemid = item.get("itemid")
            shopid = item.get("shopid")

            url = f"https://shopee.tw/product/{shopid}/{itemid}"

            results.append(Product(
                title=title,
                price=str(price),
                url=url,
                image=image,
                source="shopee"
            ))

        except:
            continue

    return results
