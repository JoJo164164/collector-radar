import streamlit as st
import pandas as pd
from scraper.py import search_all

st.set_page_config(layout="wide")

st.title("📡 Collector Radar V5")

keyword = st.text_input("搜尋商品")

sources = st.multiselect(
    "平台",
    ["shopee", "mercari", "yahoo"],
    default=["shopee", "mercari"]
)

sort = st.selectbox(
    "排序",
    ["最新", "價格低→高", "價格高→低"]
)

if st.button("搜尋"):

    data = search_all(keyword, sources)

    if not data:
        st.warning("沒有資料（可能被擋或關鍵字無結果）")
        st.stop()

    df = pd.DataFrame(data)

    if sort == "價格低→高":
        df = df.sort_values("price")
    elif sort == "價格高→低":
        df = df.sort_values("price", ascending=False)

    st.success(f"找到 {len(df)} 筆")

    cols = st.columns(3)

    for i, row in df.iterrows():

        with cols[i % 3]:

            st.markdown(f"### {row['title']}")
            st.write(f"🏪 {row['platform']}")
            st.write(f"💰 {row['price']}")

            if row["image"]:
                st.image(row["image"])

            st.write(row["time"])

            st.link_button("查看", row["url"])
