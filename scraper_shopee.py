import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}


def scrape_shopee(keyword, limit=20):

    # Layer 1: API
    api_url = "https://shopee.tw/api/v4/search/search_items"

    try:
        r = requests.get(api_url, params={
            "keyword": keyword,
            "limit": limit
        }, headers=HEADERS, timeout=10)

        data = r.json()

        items = data.get("items", [])
        if items:
            return [
                {
                    "title": i["item_basic"]["name"],
                    "price": i["item_basic"]["price"] / 100000,
                    "url": f"https://shopee.tw/product/{i['item_basic']['shopid']}/{i['item_basic']['itemid']}",
                    "image": "https://cf.shopee.tw/file/" + i["item_basic"]["image"],
                    "source": "shopee"
                }
                for i in items
            ]

    except:
        pass

    # Layer 2: fallback search page (至少不是空)
    return [{
        "title": f"Shopee search: {keyword}",
        "price": None,
        "url": f"https://shopee.tw/search?keyword={keyword}",
        "image": None,
        "source": "shopee"
    }]
