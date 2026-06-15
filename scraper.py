import requests
from datetime import datetime
import urllib.parse
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# =========================
# 工具
# =========================
def safe_float(x):
    try:
        return float(x)
    except:
        return 0.0


# =========================
# Shopee（穩定 API）
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

            basic = item.get("item_basic", {})

            title = basic.get("name", "")
            if not title:
                continue

            price = safe_float(basic.get("price", 0)) / 100000

            shop_id = basic.get("shopid")
            item_id = basic.get("itemid")

            url = f"https://shopee.tw/product/{shop_id}/{item_id}"

            image_hash = basic.get("image", "")
            image = f"https://cf.shopee.tw/file/{image_hash}" if image_hash else ""

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
# Mercari（穩定 regex）
# =========================
def search_mercari(keyword):

    try:
        url = f"https://www.mercari.com/jp/search/?keyword={urllib.parse.quote(keyword)}"

        r = requests.get(url, headers=HEADERS, timeout=10)

        items = []

        links = re.findall(r'href="(/jp/items/[^"]+)"', r.text)

        for link in links[:10]:

            items.append({
                "title": keyword,
                "price": 0,
                "platform": "Mercari",
                "url": "https://www.mercari.com" + link,
                "image": "",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        return items

    except Exception as e:
        print("Mercari error:", e)
        return []


# =========================
# Yahoo 拍賣（穩定 regex）
# =========================
def search_yahoo(keyword):

    try:
        url = f"https://tw.bid.yahoo.com/search/auction/product?p={urllib.parse.quote(keyword)}"

        r = requests.get(url, headers=HEADERS, timeout=10)

        items = []

        links = re.findall(r'href="(https://tw.bid.yahoo.com/item/[^"]+)"', r.text)

        for link in links[:10]:

            if "item" not in link:
                continue

            items.append({
                "title": keyword,
                "price": 0,
                "platform": "Yahoo",
                "url": link,
                "image": "",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        return items

    except Exception as e:
        print("Yahoo error:", e)
        return []


# =========================
# 統一入口（去重 + 補資料）
# =========================
def search_all(keyword):

    results = []

    results += search_shopee(keyword)
    results += search_mercari(keyword)
    results += search_yahoo(keyword)

    seen = set()
    clean = []

    for r in results:

        if r["url"] in seen:
            continue

        seen.add(r["url"])

        if not r.get("image"):
            r["image"] = "https://via.placeholder.com/300"

        if not r.get("price"):
            r["price"] = 0

        clean.append(r)

    return clean
