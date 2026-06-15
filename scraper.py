from datetime import datetime

def search_all(keyword):

    return [
        {
            "title": f"{keyword} - Shopee",
            "price": 1200,
            "platform": "Shopee",
            "url": f"https://shopee.tw/{keyword}",
            "image": "https://via.placeholder.com/300",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        },
        {
            "title": f"{keyword} - Mercari",
            "price": 2000,
            "platform": "Mercari",
            "url": f"https://mercari.com/{keyword}",
            "image": "https://via.placeholder.com/300",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]
