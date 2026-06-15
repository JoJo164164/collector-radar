import streamlit as st
import pandas as pd

from scraper import search_all
from repo import (
    save_products,
    get_products,
    add_favorite,
    remove_favorite
)

st.set_page_config(page_title="Collector Radar", layout="wide")

st.title("⚾ 收藏品雷達 FINAL")

# ======================
# 關鍵字
# ======================
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

# ======================
# sidebar
# ======================
category = st.sidebar.selectbox("類別", list(KEYWORDS.keys()))

view_mode = st.sidebar.radio(
    "觀看模式",
    ["全部商品", "我的最愛"]
)

sort_mode = st.sidebar.selectbox(
    "排序",
    ["最新", "價格低到高", "價格高到低"]
)

# ======================
# 更新資料
# ======================
if st.button("🔄 更新資料（抓 Shopee / Mercari / Yahoo）"):
    all_items = []

    for kw in KEYWORDS[category]:
        results = search_all(kw)
        all_items += results

    save_products(all_items)
    st.success("更新完成")

# ======================
# 讀資料
# ======================
data = get_products()
df = pd.DataFrame(data)

if not df.empty:
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0)

# ======================
# filter
# ======================
if view_mode == "我的最愛":
    df = df[df["favorite"] == True]

# ======================
# sort
# ======================
if not df.empty:
    if sort_mode == "價格低到高":
        df = df.sort_values("price")
    elif sort_mode == "價格高到低":
        df = df.sort_values("price", ascending=False)
    else:
        df = df.sort_values("time", ascending=False)

# ======================
# UI
# ======================
cols = st.columns(3)

for i, row in df.iterrows():

    with cols[i % 3]:

        st.image(row["image"])
        st.write(row["title"])
        st.write(f"💰 {row['price']}")
        st.write(f"🏪 {row['platform']}")
        st.write(f"🕒 {row['time']}")
        st.write(f"[連結]({row['url']})")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⭐ 收藏", key=f"fav_{i}"):
                add_favorite(row["url"])
                st.rerun()

        with col2:
            if st.button("❌ 取消", key=f"unfav_{i}"):
                remove_favorite(row["url"])
                st.rerun()

st.subheader("📈 價格歷史（下一版會做圖表）")
st.write("已具備資料結構，可升級價格趨勢分析")
