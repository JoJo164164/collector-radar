import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

UA = [
    "Mozilla/5.0 Chrome/122",
    "Mozilla/5.0 Chrome/121",
    "Mozilla/5.0 Safari"
]

def headers():
    return {"User-Agent": random.choice(UA)}


def fetch_html(url):
    try:
        r = requests.get(url, headers=headers(), timeout=10)
        return r.text
    except:
        return ""


# -------------------------
# Yahoo (stable)
# -------------------------
def scrape_yahoo(keyword, limit=20):
    url = f"https://tw.bid.yahoo.com/search/auction/product?p={keyword}"
    html = fetch_html(url)

    soup = BeautifulSoup(html, "lxml")
    results = []

    for a in soup.select("a"):
        t = a.get_text(strip=True)

        if len(t) < 5:
            continue

        results.append({
            "title": t,
            "price": 0,
            "platform": "Yahoo",
            "url": url,
            "image": "",
            "time": datetime.utcnow().isoformat()
        })

        if len(results) >= limit:
            break

    return results


# -------------------------
# Shopee (best-effort HTML)
# -------------------------
def scrape_shopee(keyword, limit=20):
    url = f"https://shopee.tw/search?keyword={keyword}"
    html = fetch_html(url)

    soup = BeautifulSoup(html, "lxml")

    results = []

    for a in soup.select("a"):
        t = a.get_text(strip=True)

        if len(t) < 5:
            continue

        results.append({
            "title": t,
            "price": 0,
            "platform": "Shopee",
            "url": url,
            "image": "",
            "time": datetime.utcnow().isoformat()
        })

        if len(results) >= limit:
            break

    return results


# -------------------------
# Mercari fallback
# -------------------------
def scrape_mercari(keyword):
    return []


# -------------------------
# eBay (stable)
# -------------------------
def scrape_ebay(keyword, limit=20):
    url = f"https://www.ebay.com/sch/i.html?_nkw={keyword}"
    html = fetch_html(url)

    soup = BeautifulSoup(html, "lxml")

    results = []

    for item in soup.select("li.s-item"):
        title = item.select_one(".s-item__title")
        link = item.select_one("a")

        if not title or not link:
            continue

        results.append({
            "title": title.text,
            "price": 0,
            "platform": "eBay",
            "url": link["href"],
            "image": "",
            "time": datetime.utcnow().isoformat()
        })

        if len(results) >= limit:
            break

    return results
