import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse

# =========================
# Shopee 搜尋
# =========================
def search_shopee(keyword):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        url = f"https://shopee.tw/search?keyword={urllib.parse.quote(keyword)}"

        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        items = []

        # Shopee DOM 會變動，這是「基礎抓法」
        for tag in soup.select("div[data-sqe='item']")[:10]:

            title = tag.text.strip()[:50]

            link = tag.find("a")
            url = "https://shopee.tw" + link["href"] if link else ""

            img = tag.find("img")
            image = img["src"] if img else ""

            items.append({
                "title": title,
                "price": 0,
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
# Mercari 搜尋
# =========================
def search_mercari(keyword):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        url = f"https://www.mercari.com/jp/search/?keyword={urllib.parse.quote(keyword)}"

        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        items = []

        for tag in soup.select("li.items-box")[:10]:

            title = tag.text.strip()[:50]

            link = tag.find("a")
            url = "https://www.mercari.com" + link["href"] if link else ""

            img = tag.find("img")
            image = img["data-src"] if img else ""

            items.append({
                "title": title,
                "price": 0,
                "platform": "Mercari",
                "url": url,
                "image": image,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        return items

    except Exception as e:
        print("Mercari error:", e)
        return []


# =========================
# Yahoo 拍賣（台灣）
# =========================
def search_yahoo(keyword):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        url = f"https://tw.bid.yahoo.com/search/auction/product?p={urllib.parse.quote(keyword)}"

        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")

        items = []

        for tag in soup.select("li")[:10]:

            title_tag = tag.find("a")
            if not title_tag:
                continue

            title = title_tag.text.strip()
            url = title_tag["href"]

            img = tag.find("img")
            image = img["src"] if img else ""

            items.append({
                "title": title,
                "price": 0,
                "platform": "Yahoo",
                "url": url,
                "image": image,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            })

        return items

    except Exception as e:
        print("Yahoo error:", e)
        return []


# =========================
# 統一入口
# =========================
def search_all(keyword):

    results = []

    results += search_shopee(keyword)
    results += search_mercari(keyword)
    results += search_yahoo(keyword)

    return results
