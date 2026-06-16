import random
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# =====================
# Headers
# =====================
UA = [
    "Mozilla/5.0 Chrome/122",
    "Mozilla/5.0 Chrome/121",
    "Mozilla/5.0 Safari/537.36"
]

def headers():
    return {"User-Agent": random.choice(UA)}


# =====================
# Yahoo (穩定來源)
# =====================
def scrape_yahoo(keyword, limit=30):
    url = f"https://tw.bid.yahoo.com/search/auction/product?p={keyword}"
    r = requests.get(url, headers=headers(), timeout=10)

    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "lxml")

    results = []

    for a in soup.select("a"):
        title = a.get_text(strip=True)

        if len(title) < 5:
            continue

        if keyword.lower() not in title.lower():
            continue

        results.append({
            "title": title[:100],
            "price": 0.0,
            "platform": "Yahoo",
            "url": url,
            "image": "",
            "time": datetime.utcnow().isoformat()
        })

        if len(results) >= limit:
            break

    return results


# =====================
# eBay (穩定 + 可用)
# =====================
def scrape_ebay(keyword, limit=30):
    url = f"https://www.ebay.com/sch/i.html?_nkw={keyword}"
    r = requests.get(url, headers=headers(), timeout=10)

    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "lxml")
    results = []

    for item in soup.select("li.s-item"):
        title = item.select_one(".s-item__title")
        price = item.select_one(".s-item__price")
        img = item.select_one("img")
        link = item.select_one("a")

        if not title or not link:
            continue

        results.append({
            "title": title.text,
            "price": parse_price(price.text if price else "0"),
            "platform": "eBay",
            "url": link["href"],
            "image": img["src"] if img else "",
            "time": datetime.utcnow().isoformat()
        })

        if len(results) >= limit:
            break

    return results


def parse_price(text):
    try:
        return float("".join([c for c in text if (c.isdigit() or c == ".")]))
    except:
        return 0.0


# =====================
# Shopee / Mercari（現實限制）
# =====================
def scrape_shopee(keyword):
    # JS + anti bot → 先 fallback
    return []


def scrape_mercari(keyword):
    # Cloudflare / API restricted
    return []


# =====================
# Router
# =====================
def search_all(keyword, sources):
    results = []

    if "yahoo" in sources:
        results += scrape_yahoo(keyword)

    if "ebay" in sources:
        results += scrape_ebay(keyword)

    if "shopee" in sources:
        results += scrape_shopee(keyword)

    if "mercari" in sources:
        results += scrape_mercari(keyword)

    return results
