def save_products(session, Product, items):
    for item in items:

        url = item.get("url")
        title = item.get("title")

        # ❗ 沒 url 直接跳過（避免 DB crash）
        if not url:
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
