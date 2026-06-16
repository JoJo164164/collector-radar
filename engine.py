def to_dict(p):
    return {
        "title": getattr(p, "title", None) if not isinstance(p, dict) else p.get("title"),
        "price": getattr(p, "price", None) if not isinstance(p, dict) else p.get("price"),
        "url": getattr(p, "url", None) if not isinstance(p, dict) else p.get("url"),
        "image": getattr(p, "image", None) if not isinstance(p, dict) else p.get("image"),
        "source": getattr(p, "source", None) if not isinstance(p, dict) else p.get("source"),
    }


def search_all(keyword, sources):

    results = []

    if "shopee" in sources:
        results += scrape_shopee(keyword)

    if "mercari" in sources:
        results += scrape_mercari(keyword)

    if "ebay" in sources:
        results += scrape_ebay(keyword)

    if "yahoo" in sources:
        results += scrape_yahoo(keyword)

    return [to_dict(r) for r in results]
