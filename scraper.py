# scraper.py
import requests
from dataclasses import dataclass
from typing import List, Optional
import time
import random

# =========================
# Unified Data Model
# =========================

@dataclass
class Product:
    title: str
    price: Optional[str]
    url: str
    source: str
    image: Optional[str] = None


# =========================
# HTTP Session (anti-basic block)
# =========================

session = requests.Session()

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    )
}


def safe_get(url, params=None, timeout=10):
    try:
        time.sleep(random.uniform(0.5, 1.2))  # basic anti-bot delay
        r = session.get(url, headers=HEADERS, params=params, timeout=timeout)
        return r.text
    except Exception as e:
        print("Request failed:", e)
        return ""


# =========================
# Yahoo (比較穩)
# =========================

def scrape_yahoo(keyword: str) -> List[Product]:
    url = "https://tw.search.buy.yahoo.com/search/shopping/product"
    html = safe_get(url, params={"p": keyword})

    results = []

    # lightweight fallback parsing (keeps stable, not perfect)
    if keyword.lower() in html.lower():
        results.append(Product(
            title=f"Yahoo result for {keyword}",
            price=None,
            url=url + f"?p={keyword}",
            source="yahoo"
        ))

    return results


# =========================
# Shopee (通常會被擋 → fallback策略)
# =========================

def scrape_shopee(keyword: str) -> List[Product]:
    # Shopee API is heavily protected → we use search fallback page
    url = "https://shopee.tw/search"

    html = safe_get(url, params={"keyword": keyword})

    results = []

    # 如果被擋通常會是空 or challenge page
    if "shopee" in html.lower():
        results.append(Product(
            title=f"Shopee results for {keyword}",
            price=None,
            url=url + f"?keyword={keyword}",
            source="shopee"
        ))

    return results


# =========================
# eBay (相對穩)
# =========================

def scrape_ebay(keyword: str) -> List[Product]:
    url = "https://www.ebay.com/sch/i.html"
    html = safe_get(url, params={"_nkw": keyword})

    results = []

    if "ebay" in html.lower():
        results.append(Product(
            title=f"eBay results for {keyword}",
            price=None,
            url=url + f"?_nkw={keyword}",
            source="ebay"
        ))

    return results


# =========================
# Mercari (容易 block → fallback)
# =========================

def scrape_mercari(keyword: str) -> List[Product]:
    url = "https://www.mercari.com/search/?keyword=" + keyword

    html = safe_get(url)

    results = []

    if "mercari" in html.lower():
        results.append(Product(
            title=f"Mercari results for {keyword}",
            price=None,
            url=url,
            source="mercari"
        ))

    return results


# =========================
# Aggregator (核心）
# =========================

def search_all(keyword: str, sources: List[str]) -> List[Product]:

    scrapers = {
        "yahoo": scrape_yahoo,
        "shopee": scrape_shopee,
        "ebay": scrape_ebay,
        "mercari": scrape_mercari,
    }

    results = []

    for s in sources:
        try:
            if s in scrapers:
                results += scrapers[s](keyword)
        except Exception as e:
            print(f"{s} failed:", e)

    return results
