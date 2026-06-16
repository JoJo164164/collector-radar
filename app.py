import streamlit as st
from engine import search_all

st.title("📡 Collector Radar v5 (REAL DATA)")

keyword = st.text_input("keyword")

sources = st.multiselect(
    "sources",
    ["shopee", "mercari", "ebay", "yahoo"],
    default=["shopee", "mercari", "ebay", "yahoo"]
)

if st.button("search"):

    results = search_all(keyword, sources)

    if not results:
        st.error("no results")
        st.stop()

    for r in results:
        st.markdown("---")

        st.write("🏪", r.source)
        st.write("📦", r.title)

        if r.price:
            st.write("💰", r.price)

        st.write("🔗", r.url)

        if r.image:
            st.image(r.image, width=150)
