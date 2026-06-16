import streamlit as st
from engine import search_all

st.title("📡 Collector Radar v5")

keyword = st.text_input("keyword")

sources = st.multiselect(
    "sources",
    ["shopee", "mercari", "ebay", "yahoo"],
    default=["shopee", "mercari", "ebay", "yahoo"]
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

        st.write("🏪", r.get("source", "unknown"))
        st.write("📦", r.get("title", "no title"))

        if r.get("price"):
            st.write("💰", r.get("price"))

        if r.get("image"):
            st.image(r.get("image"), width=150)

        st.write("🔗", r.get("url", ""))
