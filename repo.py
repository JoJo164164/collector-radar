from models import Product

def save_products(session, items):

    for item in items:

        if not item.get("url") or not item.get("title"):
            continue

        exists = session.query(Product).filter_by(url=item["url"]).first()
        if exists:
            continue

        session.add(Product(
            title=item["title"],
            price=float(item.get("price") or 0),
            platform=item.get("platform"),
            url=item["url"],
            image=item.get("image"),
            time=item.get("time")
        ))

    session.commit()
