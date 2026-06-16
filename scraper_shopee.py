import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_shopee(keyword, limit=20):

    url = "https://shopee.tw/api/v4/search/search_items"

    params = {
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

    for i in data.get("items", []):
        try:
            item = i["item_basic"]

            results.append({
                "title": item["name"],
                "price": item["price"] / 100000,
                "url": f"https://shopee.tw/product/{item['shopid']}/{item['itemid']}",
                "image": "https://cf.shopee.tw/file/" + item["image"],
                "source": "shopee"
            })

        except:
            continue

    return results
