from datetime import datetime

def search_all(keyword):
    """
    模擬 Shopee / Mercari / Yahoo 搜尋結果
    下一步我們才換成真爬蟲
    """

    return [
        {
            "title": f"{keyword} - Shopee sample",
            "price": 1200,
            "platform": "Shopee",
            "url": "https://shopee.tw/sample1",
            "image": "https://via.placeholder.com/300",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        },
        {
            "title": f"{keyword} - Mercari sample",
            "price": 2000,
            "platform": "Mercari",
            "url": "https://mercari.com/sample2",
            "image": "https://via.placeholder.com/300",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]
