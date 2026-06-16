from models import Product

def save_products(session, items):

    for item in items:

        if not isinstance(item, dict):
            continue

        if not item.get("url") or not item.get("title"):
            continue

        exists = session.query(Product).filter_by(url=item["url"]).first()
        if exists:
            continue

        session.add(Product(
            title=item["title"],
            url=item["url"],
            price=float(item.get("price") or 0),
            image=item.get("image") or "",
            platform=item.get("platform") or "",
            time=item.get("time") or ""
        ))

    session.commit()
