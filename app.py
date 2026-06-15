import streamlit as st
from scraper import scrape_all

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Product
from repo import save_products

# DB
engine = create_engine("sqlite:///data.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

st.title("Collector Radar")

keyword = st.text_input("keyword")

if st.button("search") and keyword:

    items = scrape_all(keyword)

    save_products(session, items)

    st.success(f"saved {len(items)} items")
