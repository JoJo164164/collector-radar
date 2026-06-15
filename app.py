import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="Collector Radar", layout="wide")

st.title("⚾ 收藏品雷達 Collector Radar")

# =========================
# 關鍵字（你指定版本）
# =========================
KEYWORDS = {
    "啦啦隊簽名球": [
        "啦啦隊簽名球",
        "女孩簽名球",
        "職籃啦啦隊簽名球"
    ],
    "棒球公仔": [
        "bobblehead",
        "搖頭公仔",
        "棒球公仔",
        "MLB bobblehead",
        "中職公仔"
    ]
}

category = st.sidebar.selectbox("搜尋類別", list(KEYWORDS.keys()))

platform = st.sidebar.multiselect(
    "平台",
    ["Shopee", "Mercari", "Yahoo"],
    default=["Shopee", "Mercari", "Yahoo"]
)

sort_by = st.sidebar.selectbox(
    "排序",
    ["最新", "價格低到高", "價格高到低"]
)

# =========================
# 先做「搜尋引擎框架」
# =========================

def search_mock(keyword, platform):
    """先用假資料，確保UI正常"""
    return [
        {
            "title": f"{keyword} sample 1",
            "price": 1000,
            "platform": platform,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "url": "https://example.com"
        }
    ]

# =========================
# 主邏輯
# =========================

results = []

for kw in KEYWORDS[category]:
    for p in platform:
        results += search_mock(kw, p)

df = pd.DataFrame(results)

# =========================
# 排序
# =========================
if sort_by == "價格低到高":
    df = df.sort_values("price")
elif sort_by == "價格高到低":
    df = df.sort_values("price", ascending=False)
else:
    df = df.sort_values("time", ascending=False)

# =========================
# 顯示
# =========================
cols = st.columns(3)

for i, row in df.iterrows():
    with cols[i % 3]:
        st.markdown("### 商品")
        st.write(row["title"])
        st.write(f"💰 {row['price']}")
        st.write(f"🏪 {row['platform']}")
        st.write(f"🕒 {row['time']}")
        st.write(f"[連結]({row['url']})")
