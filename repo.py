from db import Session, Product, PriceHistory

# ======================
# 存商品
# ======================
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

        # ⭐ 價格歷史（每次都記）
        ph = PriceHistory(
            url=item["url"],
            price=item["price"],
            time=item.get("time", "")
        )
        session.add(ph)

    session.commit()
    session.close()


# ======================
# 讀商品
# ======================
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
            "time": d.time,
            "favorite": d.favorite
        })

    session.close()
    return result


# ======================
# 收藏功能
# ======================
def add_favorite(url):
    session = Session()
    item = session.query(Product).filter_by(url=url).first()
    if item:
        item.favorite = True
    session.commit()
    session.close()


def remove_favorite(url):
    session = Session()
    item = session.query(Product).filter_by(url=url).first()
    if item:
        item.favorite = False
    session.commit()
    session.close()
