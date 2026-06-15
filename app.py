import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Collector Radar",
    layout="wide"
)

st.title("⚾ Collector Radar")

search_type = st.sidebar.selectbox(
    "收藏品類型",
    [
        "啦啦隊簽名球",
        "棒球公仔"
    ]
)

sort_option = st.sidebar.selectbox(
    "排序方式",
    [
        "最新上架",
        "價格低到高",
        "價格高到低"
    ]
)

platforms = st.sidebar.multiselect(
    "平台",
    [
        "Shopee",
        "Mercari",
        "Yahoo"
    ],
    default=["Shopee","Mercari","Yahoo"]
)

st.write("### 搜尋結果")

sample_data = [
    {
        "title":"李多慧簽名球",
        "price":5000,
        "platform":"Shopee",
        "time":"2026-06-15",
        "image":"https://via.placeholder.com/300"
    },
    {
        "title":"Ohtani Bobblehead",
        "price":3500,
        "platform":"Mercari",
        "time":"2026-06-14",
        "image":"https://via.placeholder.com/300"
    }
]

df = pd.DataFrame(sample_data)

cols = st.columns(3)

for idx,row in df.iterrows():

    with cols[idx % 3]:

        st.image(row["image"])

        st.write(row["title"])

        st.write(f"價格：{row['price']}")

        st.write(f"平台：{row['platform']}")

        st.write(f"時間：{row['time']}")
