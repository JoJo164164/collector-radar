import requests
from bs4 import BeautifulSoup
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}

def clean_price(text):
    if not text:
        return None
    match = re.findall(r"[\d,.]+", text)
    return match[0] if match else None


def scrape_shopee(keyword, limit=10):
    url = f"https://shopee.tw/api/v4/search/search_items?keyword={keyword}&limit={limit}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()

        results = []

        for i in data.get("items", []):
            item = i.get("item_basic", {})

            results.append({
                "title": item.get("name"),
                "price": item.get("price") / 100000 if item.get("price") else None,
                "image": f"https://cf.shopee.tw/file/{item.get('image')}" if item.get("image") else None,
                "url": f"https://shopee.tw/product/{item.get('shopid')}/{item.get('itemid')}"
            })

        return results
    except:
        return []


def scrape_all(keyword):
    return scrape_shopee(keyword)
