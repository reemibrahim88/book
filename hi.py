import streamlit as st
import pandas as pd
import base64

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("enhanced_books_final.csv")

# App title and layout
st.set_page_config(page_title="📚 Smart Book Finder", layout="wide")
st.title("📚 Smart Book Finder")

st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Books")
category = st.sidebar.selectbox("Category", ["All"] + sorted(df["category"].unique().tolist()))
level = st.sidebar.selectbox("Level", ["All"] + sorted(df["level"].unique().tolist()))
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.0, 0.1)
search_title = st.sidebar.text_input("Search by Title")

# Filter data
filtered_df = df.copy()
if category != "All":
    filtered_df = filtered_df[filtered_df["category"] == category]
if level != "All":
    filtered_df = filtered_df[filtered_df["level"] == level]
if search_title:
    filtered_df = filtered_df[filtered_df["title"].str.contains(search_title, case=False)]
filtered_df = filtered_df[filtered_df["user_rating"] >= min_rating]

# Display results
st.subheader(f"📖 {len(filtered_df)} Books Found")
for _, row in filtered_df.iterrows():
    with st.container():

        # Book title
        st.markdown(f"### {row['title']}")

        # Author, Year, Pages, Rating 
        st.markdown(
            f"*Author:* {row['author']}  |  "
            f"*Year:* {row['year_published']}  |  "
            f"*Pages:* {row['number_of_pages']}  |  "
            f"*Rating:* ⭐ {row['user_rating']}  |  "
        )

        st.markdown(
        f"Level: {row['level']}  |  "
        f"Category: {row['category']}"
        )

        # Summary
        with st.expander("📘 Summary"):
            st.write(row["summary of the book"])
        st.divider()

# Download filtered results as CSV
csv = filtered_df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
st.markdown(f'<a href="data:file/csv;base64,{b64}" download="filtered_books.csv">📥 Download Results as CSV</a>', unsafe_allow_html=True)
