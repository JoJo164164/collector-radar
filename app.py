import streamlit as st
import pandas as pd
from scraper import search_all

st.set_page_config(page_title="Collector Radar v3", layout="wide")

st.title("📡 Collector Radar v3")

# -------------------
# UI 控制區
# -------------------
keyword = st.text_input("搜尋商品")

sources = st.multiselect(
    "選擇平台",
    ["yahoo", "shopee", "mercari"],
    default=["yahoo", "shopee"]
)

sort_option = st.selectbox(
    "排序方式",
    ["最新", "價格低→高", "價格高→低"]
)

if st.button("搜尋"):

    data = search_all(keyword, sources)

    if not data:
        st.warning("沒有資料")
        st.stop()

    df = pd.DataFrame(data)

    # -------------------
    # 排序
    # -------------------
    if sort_option == "價格低→高":
        df = df.sort_values("price")
    elif sort_option == "價格高→低":
        df = df.sort_values("price", ascending=False)

    st.success(f"找到 {len(df)} 筆資料")

    # -------------------
    # 卡片 UI
    # -------------------
    cols = st.columns(3)

    for i, row in df.iterrows():
        with cols[i % 3]:

            st.markdown(f"### {row['title']}")
            st.write(f"🏪 {row['platform']}")
            st.write(f"💰 {row['price']}")

            if row.get("image"):
                st.image(row["image"])

            st.write(f"🕒 {row['time']}")

            st.link_button("查看商品", row["url"])
