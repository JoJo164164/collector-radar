import requests
from bs4 import BeautifulSoup
from datetime import datetime
from playwright.sync_api import sync_playwright
import random
import re

# =========================
# Headers
# =========================
UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X) Chrome/121 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) Chrome/120 Safari/537.36",
]

def headers():
    return {
        "User-Agent": random.choice(UA),
        "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
    }


# =========================
# SAFE PARSER
# =========================
def clean_price(text):
    if not text:
        return 0.0
    try:
        num = re.sub(r"[^0-9.]", "", text)
        return float(num) if num else 0.0
    except:
        return 0.0


# =========================
# PLAYWRIGHT FETCH
# =========================
def fetch_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_timeout(2500)

        html = page.content()
        browser.close()
        return html


# =========================
# SHOPEE (JS RENDERED)
# =========================
def scrape_shopee(keyword, limit=20):
    url = f"https://shopee.tw/search?keyword={keyword}"

    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")

    results = []

    # Shopee cards (best-effort parse)
    for a in soup.select("a"):
        title = a.get_text(" ", strip=True)

        if len(title) < 5:
            continue

        if keyword.lower() not in title.lower():
            continue

        img = a.find("img")

        results.append({
            "title": title[:100],
            "price": 0.0,
            "platform": "Shopee",
            "url": url,
            "image": img["src"] if img and img.get("src") else "",
            "time": datetime.utcnow().isoformat()
        })

        if len(results) >= limit:
            break

    return results


# =========================
# MERCARI (JS RENDERED)
# =========================
def scrape_mercari(keyword, limit=20):
    url = f"https://www.mercari.com/jp/search/?keyword={keyword}"

    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")

    results = []

    for a in soup.select("a"):
        text = a.get_text(" ", strip=True)

        if len(text) < 5:
            continue

        if keyword.lower() not in text.lower():
            continue

        img = a.find("img")

        href = a.get("href", "")
        if not href:
            continue

        if href.startswith("/"):
            href = "https://www.mercari.com" + href

        results.append({
            "title": text[:100],
            "price": 0.0,
            "platform": "Mercari",
            "url": href,
            "image": img["src"] if img and img.get("src") else "",
            "time": datetime.utcnow().isoformat()
        })

        if len(results) >= limit:
            break

    return results


# =========================
# YAHOO (requests)
# =========================
def scrape_yahoo(keyword, limit=20):
    url = f"https://tw.bid.yahoo.com/search/auction/product?p={keyword}"

    try:
        r = requests.get(url, headers=headers(), timeout=10)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, "lxml")
        results = []

        for a in soup.select("a"):
            title = a.get_text(" ", strip=True)

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

    except:
        return []


# =========================
# EBAY (requests stable)
# =========================
def scrape_ebay(keyword, limit=20):
    url = f"https://www.ebay.com/sch/i.html?_nkw={keyword}"

    try:
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
                "title": title.text.strip(),
                "price": clean_price(price.text if price else ""),
                "platform": "eBay",
                "url": link["href"],
                "image": img["src"] if img else "",
                "time": datetime.utcnow().isoformat()
            })

            if len(results) >= limit:
                break

        return results

    except:
        return []


# =========================
# ROUTER
# =========================
def search_all(keyword, sources=None):
    sources = sources or ["shopee", "mercari", "yahoo", "ebay"]

    results = []

    if "shopee" in sources:
        results += scrape_shopee(keyword)

    if "mercari" in sources:
        results += scrape_mercari(keyword)

    if "yahoo" in sources:
        results += scrape_yahoo(keyword)

    if "ebay" in sources:
        results += scrape_ebay(keyword)

    return results
