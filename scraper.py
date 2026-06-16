import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime

HEADERS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X) Chrome/121 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36",
]

def headers():
    return {
        "User-Agent": random.choice(HEADERS_LIST),
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    }


# -------------------------
# Yahoo (相對穩)
# -------------------------
def scrape_yahoo(keyword, limit=20):
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
            "title": title[:80],
            "price": 0,
            "platform": "Yahoo",
            "url": url,
            "image": "",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        if len(results) >= limit:
            break

    return results


# -------------------------
# Shopee（fallback）
# -------------------------
def scrape_shopee(keyword, limit=20):
    url = f"https://shopee.tw/search?keyword={keyword}"
    r = requests.get(url, headers=headers(), timeout=10)

    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "lxml")
    results = []

    for a in soup.select("a"):
        text = a.get_text(strip=True)

        if len(text) < 5:
            continue

        if keyword.lower() not in text.lower():
            continue

        results.append({
            "title": text[:80],
            "price": 0,
            "platform": "Shopee",
            "url": url,
            "image": "",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        if len(results) >= limit:
            break

    return results


# -------------------------
# Mercari（先 fallback）
# -------------------------
def scrape_mercari(keyword):
    return []


def search_all(keyword, sources=None):
    sources = sources or ["yahoo", "shopee"]

    all_data = []

    if "yahoo" in sources:
        all_data += scrape_yahoo(keyword)

    if "shopee" in sources:
        all_data += scrape_shopee(keyword)

    if "mercari" in sources:
        all_data += scrape_mercari(keyword)

    return all_data
