import streamlit as st
from engine import search_all

st.title("📡 Collector Radar (No Install / No Browser)")

keyword = st.text_input("keyword")

sources = st.multiselect(
    "sources",
    ["yahoo", "ebay", "shopee", "mercari"],
    default=["yahoo", "ebay", "shopee", "mercari"]
)

if st.button("search"):

    if not keyword:
        st.warning("enter keyword")
        st.stop()

    results = search_all(keyword, sources)

    if not results:
        st.error("no results")
        st.stop()

    for r in results:
        st.markdown("---")
        st.write("🏪", r["source"])
        st.write("📦", r["title"])
        st.write("🔗", r["url"])
