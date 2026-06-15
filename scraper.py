import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

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

        items = data.get("items", [])
        results = []

        for i in items:
            item = i.get("item_basic", {})
            results.append({
                "title": item.get("name"),
                "price": item.get("price") / 100000 if item.get("price") else None,
                "image": f"https://cf.shopee.tw/file/{item.get('image')}",
                "url": f"https://shopee.tw/product/{item.get('shopid')}/{item.get('itemid')}"
            })

        return results
    except Exception as e:
        print("Shopee error:", e)
        return []


def scrape_yahoo(keyword):
    url = f"https://tw.search.yahoo.com/search?p={keyword}+拍賣"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        for card in soup.select("div.dd.algo"):
            title_tag = card.select_one("h3")
            link_tag = card.select_one("a")

            if not title_tag or not link_tag:
                continue

            results.append({
                "title": title_tag.text.strip(),
                "price": None,
                "image": None,
                "url": link_tag["href"]
            })

        return results[:10]
    except Exception as e:
        print("Yahoo error:", e)
        return []


def scrape_mercari(keyword):
    url = f"https://www.mercari.com/search/?keyword={keyword}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []

        for card in soup.select("li.items-box"):
            title = card.select_one(".items-box-name")
            price = card.select_one(".items-box-price")
            img = card.select_one("img")
            link = card.select_one("a")

            if not title:
                continue

            results.append({
                "title": title.text.strip(),
                "price": clean_price(price.text if price else ""),
                "image": img["data-src"] if img and img.get("data-src") else None,
                "url": "https://www.mercari.com" + link["href"] if link else None
            })

        return results[:10]
    except Exception as e:
        print("Mercari error:", e)
        return []


def search_all(keyword):
    return {
        "shopee": scrape_shopee(keyword),
        "yahoo": scrape_yahoo(keyword),
        "mercari": scrape_mercari(keyword)
    }
