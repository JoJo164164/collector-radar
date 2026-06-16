import requests

def scrape_mercari(keyword, limit=20):

    url = "https://www.mercari.com/us/api/v2/search"

    params = {
        "keyword": keyword,
        "page_size": limit
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
    except:
        return []

    results = []

    for item in data.get("items", []):
        try:
            results.append({
                "title": item["name"],
                "price": item.get("price"),
                "url": "https://www.mercari.com/us/item/" + item["id"],
                "image": item.get("photo_url"),
                "source": "mercari"
            })

        except:
            continue

    return results
