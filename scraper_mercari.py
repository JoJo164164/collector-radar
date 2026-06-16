import requests

def scrape_mercari(keyword, limit=20):

    url = "https://www.mercari.com/us/api/v2/search"

    try:
        r = requests.get(url, params={
            "keyword": keyword,
            "page_size": limit
        }, timeout=10)

        data = r.json()

        items = data.get("items", [])

        if items:
            return [
                {
                    "title": i["name"],
                    "price": i.get("price"),
                    "url": "https://www.mercari.com/us/item/" + i["id"],
                    "image": i.get("photo_url"),
                    "source": "mercari"
                }
                for i in items
            ]

    except:
        pass

    return [{
        "title": f"Mercari search: {keyword}",
        "price": None,
        "url": f"https://www.mercari.com/search/?keyword={keyword}",
        "image": None,
        "source": "mercari"
    }]
