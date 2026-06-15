import streamlit as st
from scraper import scrape_all

st.set_page_config(
    page_title="Collector Radar",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Collector Radar")
st.caption("Shopee / Yahoo / Mercari 收藏品搜尋器")

keyword = st.text_input(
    "搜尋關鍵字",
    placeholder="例如：搖頭公仔、寶可夢卡、Hot Toys"
)

if st.button("搜尋"):

    if not keyword.strip():
        st.warning("請輸入搜尋關鍵字")
        st.stop()

    with st.spinner("搜尋中..."):

        items = scrape_all(keyword)

    # =====================
    # DEBUG 區
    # =====================
    with st.expander("DEBUG 資料"):

        st.write("Type:")
        st.write(type(items))

        st.write("Count:")
        st.write(len(items))

        st.write("Raw Data:")
        st.json(items)

    # =====================
    # 結果區
    # =====================

    st.subheader(f"找到 {len(items)} 筆資料")

    if len(items) == 0:

        st.error("沒有抓到任何商品")

        st.info(
            """
可能原因：

1. Shopee API 已失效
2. Shopee 擋掉 Streamlit Cloud IP
3. scraper.py 回傳空陣列
4. 搜尋字串沒有結果
            """
        )

        st.stop()

    cols = st.columns(4)

    for idx, item in enumerate(items):

        with cols[idx % 4]:

            image = item.get("image")
            title = item.get("title", "No Title")
            price = item.get("price")
            source = item.get("source", "Unknown")
            url = item.get("url")

            if image:
                try:
                    st.image(
                        image,
                        use_container_width=True
                    )
                except:
                    st.warning("圖片載入失敗")

            st.markdown(f"**{title}**")

            if price:
                st.success(f"💰 {price}")

            st.caption(source)

            if url:
                st.link_button(
                    "查看商品",
                    url
                )
