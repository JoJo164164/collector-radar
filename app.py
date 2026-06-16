# app.py
import streamlit as st
from scraper import search_all

st.set_page_config(page_title="Collector Radar v3", layout="wide")

st.title("📡 Collector Radar v3 (Multi-market search)")

# =========================
# Input
# =========================

keyword = st.text_input("Search product keyword", "")

sources = st.multiselect(
    "Select platforms",
    ["yahoo", "shopee", "ebay", "mercari"],
    default=["yahoo", "shopee", "ebay", "mercari"]
)

# =========================
# Search Button
# =========================

if st.button("Search"):

    if not keyword:
        st.warning("Please enter keyword")
        st.stop()

    with st.spinner("Searching..."):

        results = search_all(keyword, sources)

    # =========================
    # No results handling
    # =========================

    if not results:
        st.error("No results found (可能被 blocking 或無資料)")
        st.stop()

    # =========================
    # Render results
    # =========================

    st.success(f"Found {len(results)} results")

    for r in results:

        st.markdown("---")

        st.subheader(r.title)

        col1, col2 = st.columns([1, 3])

        with col1:
            st.write("🏪", r.source)

        with col2:
            if r.price:
                st.write("💰", r.price)

            st.write("🔗", r.url)
