import streamlit as st
import pandas as pd
from scraper import search_all
from repo import save_products, get_products

st.set_page_config(page_title="Collector Radar", layout="wide")

st.title("⚾ 收藏品雷達（B版歷史系統）")

KEYWORDS = {
    "啦啦隊簽名球": [
        "啦啦隊簽名球",
        "女孩簽名球",
        "職籃啦啦隊簽名球"
    ],
    "棒球公仔": [
        "bobblehead",
        "搖頭公仔",
        "棒球公仔",
        "MLB bobblehead",
        "中職公仔"
    ]
}

category = st.sidebar.selectbox("類別", list(KEYWORDS.keys()))

if st.button("🔄 更新資料（抓新商品）"):

    all_items = []

    for kw in KEYWORDS[category]:
        results = search_all(kw)
        all_items += results

    save_products(all_items)

    st.success("更新完成")

# 讀取歷史資料
data = get_products()
df = pd.DataFrame(data)

# 排序
sort = st.sidebar.selectbox(
    "排序",
    ["最新", "價格低到高", "價格高到低"]
)

if not df.empty:
    if sort == "價格低到高":
        df = df.sort_values("price")
    elif sort == "價格高到低":
        df = df.sort_values("price", ascending=False)

cols = st.columns(3)

for i, row in df.iterrows():
    with cols[i % 3]:
        st.image(row["image"])
        st.write(row["title"])
        st.write(f"💰 {row['price']}")
        st.write(f"🏪 {row['platform']}")
        st.write(f"🕒 {row['time']}")
        st.write(f"[連結]({row['url']})")
