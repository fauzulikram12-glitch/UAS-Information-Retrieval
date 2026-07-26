import json
import os
import streamlit as st
import pandas as pd

st.set_page_config(page_title="BookScrape - Book Catalog", page_icon="\U0001F4DA", layout="wide")

st.title("\U0001F4DA BookScrape - Book Catalog")
st.markdown("Data hasil web scraping dari [books.toscrape.com](http://books.toscrape.com) menggunakan **Scrapy**.")

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "books.json")


@st.cache_data
def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["price_num"] = df["price"].str.replace(r"[^\d.]", "", regex=True).astype(float)
    return df


df = load_data()

RATING_LABELS = {1: "One Star", 2: "Two Stars", 3: "Three Stars", 4: "Four Stars", 5: "Five Stars"}

col1, col2, col3, col4 = st.columns(4)

with col1:
    search_title = st.text_input("Search by Title", "")

with col2:
    price_range = st.slider(
        "Price Range",
        min_value=float(df["price_num"].min()),
        max_value=float(df["price_num"].max()),
        value=(float(df["price_num"].min()), float(df["price_num"].max())),
    )

with col3:
    rating_options = sorted(df["rating"].unique())
    selected_ratings = st.multiselect(
        "Rating",
        options=rating_options,
        default=rating_options,
        format_func=lambda x: RATING_LABELS.get(x, str(x)),
    )

with col4:
    availability_options = df["availability"].unique().tolist()
    selected_availability = st.multiselect(
        "Availability",
        options=availability_options,
        default=availability_options,
    )

filtered = df[
    (df["title"].str.contains(search_title, case=False, na=False))
    & (df["price_num"] >= price_range[0])
    & (df["price_num"] <= price_range[1])
    & (df["rating"].isin(selected_ratings))
    & (df["availability"].isin(selected_availability))
]

st.markdown(f"### Showing **{len(filtered)}** of **{len(df)}** books")

if not filtered.empty:
    display_df = filtered[["title", "price", "rating", "availability", "link"]].copy()
    display_df.columns = ["Title", "Price", "Rating", "Availability", "Link"]
    display_df["Rating"] = display_df["Rating"].map(RATING_LABELS)
    display_df["Link"] = display_df["Link"].apply(lambda x: f"[View]({x})")
    st.markdown(display_df.to_markdown(index=False), unsafe_allow_html=True)
else:
    st.warning("No books match the selected filters.")
