import streamlit as st
from scraper import scrape_all

st.set_page_config(
    page_title="Collector Radar",
    layout="wide"
)

st.title("🔍 Collector Radar")

keyword = st.text_input(
    "搜尋收藏品",
    placeholder="例如：搖頭公仔、寶可夢卡、Hot Toys"
)

if st.button("搜尋"):

    with st.spinner("搜尋中..."):

        items = scrape_all(keyword)

    st.write(f"找到 {len(items)} 筆資料")

    if len(items) == 0:
        st.warning("沒有找到任何商品")
        st.stop()

    cols = st.columns(4)

    for idx, item in enumerate(items):

        with cols[idx % 4]:

            if item.get("image"):
                st.image(
                    item["image"],
                    use_container_width=True
                )

            st.markdown(
                f"**{item.get('title','No Title')}**"
            )

            if item.get("price"):
                st.markdown(
                    f"💰 {item['price']}"
                )

            if item.get("source"):
                st.caption(
                    item["source"]
                )

            if item.get("url"):
                st.link_button(
                    "查看商品",
                    item["url"]
                )
