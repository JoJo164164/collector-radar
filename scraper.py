import requests
from datetime import datetime
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0"}


def search_shopee(keyword):
    try:
        url = "https://shopee.tw/api/v4/search/search_items"

        params = {
            "by": "relevancy",
            "keyword": keyword,
            "limit": 5,
            "newest": 0,
            "order": "desc",
            "page_type": "search"
        }

        r = requests.get(url, params=params, headers=HEADERS, timeout=10)

        print("Shopee status:", r.status_code)

        data = r.json()

        print("Shopee keys:", data.keys())

        items = []

        for item in data.get("items", []):
            basic = item.get("item_basic", {})

            print("Shopee item:", basic.get("name"))

            shop_id = basic.get("shopid")
            item_id = basic.get("itemid")

            items.append({
                "title": basic.get("name", "no title"),
                "price": basic.get("price", 0) / 100000,
                "platform": "Shopee",
                "url": f"https://shopee.tw/product/{shop_id}/{item_id}",
                "image": "",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        return items

    except Exception as e:
        print("Shopee ERROR:", e)
        return []


def search_mercari(keyword):
    return []  # 先關掉（避免干擾）


def search_yahoo(keyword):
    return [{
        "title": keyword,
        "price": 0,
        "platform": "Yahoo",
        "url": "https://tw.bid.yahoo.com",
        "image": "",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }]


def search_all(keyword):
    results = []
    results += search_shopee(keyword)
    results += search_mercari(keyword)
    results += search_yahoo(keyword)
    return results
