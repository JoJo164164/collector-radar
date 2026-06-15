def safe_float(x):
    try:
        return float(x)
    except:
        return 0.0
import requests
from datetime import datetime
import urllib.parse

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# =========================
# Shopee（改 JSON API）
# =========================
def search_shopee(keyword):

    try:
        url = "https://shopee.tw/api/v4/search/search_items"

        params = {
            "by": "relevancy",
            "keyword": keyword,
            "limit": 20,
            "newest": 0,
            "order": "desc",
            "page_type": "search"
        }

        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = r.json()

        items = []

        for item in data.get("items", []):

            item_basic = item.get("item_basic", {})

            title = item_basic.get("name", "")
            price = item_basic.get("price", 0) / 100000
            shop_id = item_basic.get("shopid")
            item_id = item_basic.get("itemid")

            url = f"https://shopee.tw/product/{shop_id}/{item_id}"

            image = "https://cf.shopee.tw/file/" + item_basic.get("image", "")

            items.append({
                "title": title,
                "price": price,
                "platform": "Shopee",
                "url": url,
                "image": image,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        return items

    except Exception as e:
        print("Shopee error:", e)
        return []


# =========================
# Mercari（穩定 HTML selector）
# =========================
def search_mercari(keyword):

    try:
        url = f"https://www.mercari.com/jp/search/?keyword={urllib.parse.quote(keyword)}"

        r = requests.get(url, headers=HEADERS, timeout=10)

        items = []

        # Mercari 常用穩定 class（比舊版可靠）
        import re

        for match in re.findall(r'href="(/jp/items/[^"]+)"', r.text)[:10]:

            item_url = "https://www.mercari.com" + match

            items.append({
                "title": keyword,
                "price": 0,
                "platform": "Mercari",
                "url": item_url,
                "image": "https://via.placeholder.com/300",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        return items

    except Exception as e:
        print("Mercari error:", e)
        return []


# =========================
# Yahoo 拍賣（穩定 link 抓法）
# =========================
def search_yahoo(keyword):

    try:
        url = f"https://tw.bid.yahoo.com/search/auction/product?p={urllib.parse.quote(keyword)}"

        r = requests.get(url, headers=HEADERS, timeout=10)

        import re

        items = []

        links = re.findall(r'href="(https://tw.bid.yahoo.com/item/[^"]+)"', r.text)

        for link in links[:10]:

            items.append({
                "title": keyword,
                "price": 0,
                "platform": "Yahoo",
                "url": link,
                "image": "https://via.placeholder.com/300",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        return items

    except Exception as e:
        print("Yahoo error:", e)
        return []


# =========================
# 統一入口
# =========================
def search_all(keyword):

    results = []

    results += search_shopee(keyword)
    results += search_mercari(keyword)
    results += search_yahoo(keyword)

    # 去重（超重要）
    seen = set()
    unique = []

    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    return unique
