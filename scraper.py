import streamlit as st
from scraper import search_all

st.set_page_config(page_title="Market Scraper", layout="wide")

st.title("🛒 Multi Marketplace Scraper (Shopee / Yahoo / Mercari)")

keyword = st.text_input("輸入搜尋關鍵字")

if st.button("開始搜尋") and keyword:
    data = search_all(keyword)

    for platform, items in data.items():
        st.subheader(f"📦 {platform.upper()}")

        if not items:
            st.warning("沒有資料")
            continue

        cols = st.columns(3)

        for idx, item in enumerate(items):
            with cols[idx % 3]:

                # 圖片防呆（避免 broken image）
                if item.get("image"):
                    st.image(item["image"], use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/300x200?text=No+Image", use_container_width=True)

                st.markdown(f"**{item.get('title', 'No title')}**")

                if item.get("price"):
                    st.write(f"💰 {item['price']}")

                if item.get("url"):
                    st.markdown(f"[👉 連結]({item['url']})")
