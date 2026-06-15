from db import Session, Product

def save_products(items):
    session = Session()

    for item in items:
        exists = session.query(Product).filter_by(url=item["url"]).first()

        if not exists:
            p = Product(
                title=item["title"],
                price=item["price"],
                platform=item["platform"],
                url=item["url"],
                image=item.get("image", ""),
                time=item.get("time", "")
            )
            session.add(p)

    session.commit()
    session.close()


def get_products():
    session = Session()
    data = session.query(Product).all()

    result = []
    for d in data:
        result.append({
            "title": d.title,
            "price": d.price,
            "platform": d.platform,
            "url": d.url,
            "image": d.image,
            "time": d.time
        })

    session.close()
    return result
