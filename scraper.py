from bs4 import BeautifulSoup
from browser import fetch_html
from datetime import datetime
import json


def scrape_shopee(keyword, limit=20):

    url = f"https://shopee.tw/search?keyword={keyword}"

    html = fetch_html(url)

    soup = BeautifulSoup(html, "lxml")

    results = []

    # Shopee 2026 DOM (JSON embedded)
    scripts = soup.find_all("script")

    for s in scripts:
        if "itemCardList" in str(s):
            try:
                text = str(s)
                start = text.find("{")
                data = json.loads(text[start:])

                items = data.get("items", [])

                for i in items[:limit]:

                    item = i.get("item_basic", {})

                    results.append({
                        "title": item.get("name"),
                        "price": item.get("price") / 100000,
                        "platform": "Shopee",
                        "url": "https://shopee.tw/product/" + str(item.get("itemid")),
                        "image": "https://cf.shopee.tw/file/" + item.get("image"),
                        "time": datetime.utcnow().isoformat()
                    })

                break

            except:
                continue

    return results
