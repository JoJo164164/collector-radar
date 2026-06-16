import requests
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def fetch(url):
    try:
        return requests.get(url, headers=HEADERS, timeout=10).text
    except:
        return ""


# ======================
# Yahoo (最穩)
# ======================

def scrape_yahoo(keyword):
    url = f"https://tw.search.yahoo.com/search?p={quote(keyword)}"
    html = fetch(url)

    return [{
        "title": f"Yahoo search: {keyword}",
        "url": url,
        "source": "yahoo"
    }]


# ======================
# eBay (可解析)
# ======================

def scrape_ebay(keyword):
    url = f"https://www.ebay.com/sch/i.html?_nkw={quote(keyword)}"
    html = fetch(url)

    return [{
        "title": f"eBay search: {keyword}",
        "url": url,
        "source": "ebay"
    }]


# ======================
# Shopee (只能 search link)
# ======================

def scrape_shopee(keyword):
    url = f"https://shopee.tw/search?keyword={quote(keyword)}"
    html = fetch(url)

    return [{
        "title": f"Shopee search: {keyword}",
        "url": url,
        "source": "shopee"
    }]


# ======================
# Mercari (只能 search link)
# ======================

def scrape_mercari(keyword):
    url = f"https://www.mercari.com/search/?keyword={quote(keyword)}"
    html = fetch(url)

    return [{
        "title": f"Mercari search: {keyword}",
        "url": url,
        "source": "mercari"
    }]
