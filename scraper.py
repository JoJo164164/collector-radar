import requests
from bs4 import BeautifulSoup
import random
import time

HEADERS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
]

def get_headers():
    return {
        "User-Agent": random.choice(HEADERS_LIST),
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
        "referer": "https://www.google.com/",
    }


# -------------------------
# SHOPEE (web fallback HTML)
# -------------------------
def scrape_shopee(keyword, limit=20):
    url = f"https://shopee.tw/search?keyword={keyword}"

    try:
        r = requests.get(url, headers=get_headers(), timeout=10)

        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, "html.parser")

        results = []

        # Shopee DOM 常變 => 用「保守抓 title + price pattern」
        for item in soup.select("div, a"):
            text = item.get_text(" ", strip=True)

            if keyword.lower() in text.lower() and len(text) < 200:
                results.append({
                    "title": text[:80],
                    "price": "N/A",
                    "source": "Shopee",
                    "url": url
                })

            if len(results) >= limit:
                break

        return results

    except Exception as e:
        print("Shopee error:", e)
        return []


# -------------------------
# YAHOO AUCTION (TW stable)
# -------------------------
def scrape_yahoo(keyword, limit=20):
    url = f"https://tw.bid.yahoo.com/search/auction/product?p={keyword}"

    try:
        r = requests.get(url, headers=get_headers(), timeout=10)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        for a in soup.select("a"):
            text = a.get_text(" ", strip=True)

            if keyword in text and len(text) < 120:
                results.append({
                    "title": text,
                    "price": "N/A",
                    "source": "Yahoo",
                    "url": url
                })

            if len(results) >= limit:
                break

        return results

    except Exception as e:
        print("Yahoo error:", e)
        return []


# -------------------------
# MERCARI (usually blocked → fallback only)
# -------------------------
def scrape_mercari(keyword):
    # Mercari 幾乎 100% 擋 server request
    # 所以直接 fallback mock or skip
    return []


# -------------------------
# MASTER AGGREGATOR
# -------------------------
def search_all(keyword):
    time.sleep(random.uniform(0.3, 1.2))

    shopee = scrape_shopee(keyword)
    yahoo = scrape_yahoo(keyword)
    mercari = scrape_mercari(keyword)

    all_results = shopee + yahoo + mercari

    # 去重
    seen = set()
    cleaned = []
    for r in all_results:
        if r["title"] not in seen:
            cleaned.append(r)
            seen.add(r["title"])

    return cleaned
