import requests
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def clean_price(text):
    if not text:
        return None

    match = re.findall(r"[\d,.]+", str(text))
    return match[0] if match else None


def scrape_shopee(keyword, limit=10):

    url = (
        f"https://shopee.tw/api/v4/search/search_items"
        f"?keyword={keyword}&limit={limit}"
    )

    try:

        r = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        print("==========")
        print("STATUS:", r.status_code)
        print("URL:", url)
        print("RESPONSE:", r.text[:500])
        print("==========")

        if r.status_code != 200:
            return []

        data = r.json()

        if "items" not in data:
            print("No items field found")
            return []

        results = []

        for row in data.get("items", []):

            item = row.get("item_basic", {})

            results.append(
                {
                    "title": item.get("name"),
                    "price": (
                        item.get("price") / 100000
                        if item.get("price")
                        else None
                    ),
                    "image": (
                        f"https://cf.shopee.tw/file/{item.get('image')}"
                        if item.get("image")
                        else None
                    ),
                    "url": (
                        f"https://shopee.tw/product/"
                        f"{item.get('shopid')}/"
                        f"{item.get('itemid')}"
                    ),
                    "source": "Shopee"
                }
            )

        print(f"Found {len(results)} items")

        return results

    except Exception as e:

        print("Shopee Error:", str(e))

        return []


def scrape_all(keyword):

    results = []

    results.extend(
        scrape_shopee(keyword)
    )

    return results
