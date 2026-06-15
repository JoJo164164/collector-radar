import streamlit as st
from scraper import search_all

st.set_page_config(page_title="Collector Radar", layout="wide")

st.title("📡 Collector Radar v3")

keyword = st.text_input("輸入搜尋關鍵字")

if st.button("開始搜尋"):
    with st.spinner("搜尋中..."):

        data = search_all(keyword)

        if not data:
            st.error("沒有抓到任何資料（來源可能被擋或DOM變更）")
            st.stop()

        st.success(f"找到 {len(data)} 筆資料")

        for item in data:
            st.markdown(f"""
            ### {item['title']}
            - 💰 {item['price']}
            - 🏪 {item['source']}
            - 🔗 {item['url']}
            """)
