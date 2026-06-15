from models import Product

def save_products(session, items):
    for item in items:

        if not isinstance(item, dict):
            continue

        url = item.get("url")
        title = item.get("title")

        # 防呆
        if not url or not title:
            continue

        exists = session.query(Product).filter_by(url=url).first()
        if exists:
            continue

        product = Product(
            title=title,
            url=url,
            price=item.get("price"),
            image=item.get("image")
        )

        session.add(product)

    session.commit()
