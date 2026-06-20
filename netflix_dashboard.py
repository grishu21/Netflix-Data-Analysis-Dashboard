import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud

st.set_page_config(page_title=" NETFLIX DATA INSIGHTS", layout="wide")
sns.set_style("whitegrid")

# --- DASHBOARD TITLE ---
dashboard_title = """
<div style="text-align: center; padding: 1em; 
            background: linear-gradient(90deg, #e50914 60%, #221f1f 100%);
            border-radius: 18px; margin-bottom:1.5em;">
    <h1 style='font-size:2.9em; font-weight:900; letter-spacing:2px; margin-bottom:6px; color:white;'>
        <span style="color:white; text-shadow:2px 2px 8px #e50914, 1px 1px 2px #000;">NETFLIX</span> 
        <span style="color:#fff700;">DATA INSIGHTS DASHBOARD 📊</span>
    </h1>
    <p style='color: #fff; font-size:1.12em;'>
      🎬 Explore Interactive Visuals: Content Trends, Genres, Directors and More!
    </p>
</div>
"""
st.markdown(dashboard_title, unsafe_allow_html=True)


# --- DATA LOADING ---
@st.cache(suppress_st_warning=True)
def load_data():
    df = pd.read_csv("netflix_cleaned.csv")
    def to_list(x):
        if isinstance(x, str):
            return [g.strip() for g in x.strip("[]").replace("'", "").split(",") if g.strip()]
        elif isinstance(x, list):
            return x
        else:
            return []
    df['all_genres'] = df['all_genres'].apply(to_list)
    return df

data = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔎 Filter Netflix Data")
years = sorted(data['year_added'].dropna().unique())
selected_years = st.sidebar.multiselect("Year Added", years, default=years)
countries = sorted(data['country'].unique())
selected_countries = st.sidebar.multiselect("Country", countries, default=countries)
all_genres = sorted(set([g for sublist in data['all_genres'] for g in sublist if g]))
selected_genres = st.sidebar.multiselect("Genre", all_genres, default=all_genres)

filtered = data[
    data['year_added'].isin(selected_years) &
    data['country'].isin(selected_countries) &
    data['all_genres'].apply(lambda gs: any(g in selected_genres for g in gs))
]

# --- METRICS ROW ---
col1, col2, col3 = st.columns(3)
col1.metric("🍿 Total Titles", filtered.shape[0])
col2.metric("🎬 Movies", filtered[filtered['type'] == "Movie"].shape[0])
col3.metric("📺 TV Shows", filtered[filtered['type'] == "TV Show"].shape[0])
st.markdown('<hr style="border-top: 2px solid #e50914;">', unsafe_allow_html=True)

# --- HELPER FUNCTION FOR PIE CHARTS ---
def pie_top5_other(value_counts, title):
    top_n = 5
    df = pd.DataFrame(value_counts.items() if isinstance(value_counts, dict) else value_counts.items(),
                      columns=["Label", "Count"]).sort_values("Count", ascending=False)
    top = df.head(top_n)
    other = df.iloc[top_n:, 1].sum()
    labels = list(top["Label"]) + (["Other"] if other > 0 else [])
    counts = list(top["Count"]) + ([other] if other > 0 else [])
    # Strong, Netflix-branded high-contrast palette (no yellow!)
    custom_pie_colors = ["#e50914", "#0080ff", "#16c172", "#f67280", "#22223b", "#f8961e"]
    colors = custom_pie_colors[:len(labels)]
    explode = [0.08] * len(labels)
    fig, ax = plt.subplots(figsize=(8, 5))
    wedges, texts, autotexts = ax.pie(
        counts, labels=labels, autopct="%1.1f%%",
        startangle=150, explode=explode, colors=colors,
        textprops={'fontsize': 12, 'weight': 'bold', 'color': 'white'}
    )
    plt.setp(autotexts, size=13, weight="bold")
    ax.set_title(title, fontsize=16, fontweight='bold', color="#e50914")
    ax.axis('equal')
    st.pyplot(fig)
    plt.clf()

# --- 1. Content Type Distribution ---
st.subheader("1. Content Type Distribution")
ct_counts = filtered['type'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(ct_counts, labels=ct_counts.index, autopct='%1.1f%%', startangle=90,
        colors=['#e50914', '#0080ff'], textprops={'color': "w", 'fontsize':14})
ax1.set_title("Content Type: Pie Chart", color="#e50914", fontweight="bold")
ax1.axis('equal')
st.pyplot(fig1)
plt.clf()

fig2, ax2 = plt.subplots()
sns.countplot(x='type', data=filtered, palette=['#e50914', '#0080ff'], ax=ax2)
ax2.set_title("Content Type: Bar Chart", fontsize=15, color="#e50914")
for p in ax2.patches:
    ax2.annotate(f'{p.get_height()}', (p.get_x() + 0.3, p.get_height() + 1), color="#e50914", weight="bold")
st.pyplot(fig2)
plt.clf()

# --- 2. Top 10 Genres ---
st.subheader("2. Top 10 Genres")
genre_counts = Counter([g for sublist in filtered['all_genres'] for g in sublist if g])
gdf = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count']).sort_values("Count", ascending=False)

fig3, ax3 = plt.subplots(figsize=(10,6))
sns.barplot(x='Count', y='Genre', data=gdf.head(10), palette="mako", ax=ax3)
ax3.set_title("Top 10 Genres (Bar Chart)", fontsize=15, color="#e50914")
for i, v in enumerate(gdf['Count'].head(10)):
    ax3.text(v+0.5, i, str(v), color="#e50914", fontweight="bold")
st.pyplot(fig3)
plt.clf()

pie_top5_other(dict(genre_counts), "Top 5 Genres (Pie Chart)")

# --- 3. Content Added Over Time ---
st.subheader("3. Content Added Over Time")
by_year = filtered['year_added'].value_counts().sort_index()
fig4, ax4 = plt.subplots(figsize=(12,5))
ax4.plot(by_year.index, by_year.values, color="#e50914", marker='o', linewidth=3)
ax4.fill_between(by_year.index, by_year.values, color="#e50914", alpha=0.19)
ax4.set_title("Titles Added Per Year", fontsize=16, color="#e50914")
ax4.set_ylabel("Number of Titles")
ax4.set_xlabel("Year Added")
ax4.grid(True, alpha=0.3)
for i, v in enumerate(by_year.values):
    ax4.text(list(by_year.index)[i], v + 2, str(v), ha='center', fontsize=9, color="#e50914")
st.pyplot(fig4)
plt.clf()

# --- 4. Top 10 Directors ---
st.subheader("4. Top 10 Directors")
if "director" in filtered.columns:
    d_counts = filtered['director'].value_counts().head(10)
    fig5, ax5 = plt.subplots(figsize=(10,6))
    sns.barplot(x=d_counts.values, y=d_counts.index, palette="rocket", ax=ax5)
    ax5.set_title("Top 10 Directors", fontsize=16, color="#e50914")
    ax5.set_xlabel("Number of Titles")
    ax5.set_ylabel("Director")
    for i, v in enumerate(d_counts.values):
        ax5.text(v + 0.5, i, str(v), va='center', fontweight='bold', color="#e50914")
    st.pyplot(fig5)
    plt.clf()
else:
    st.warning("No 'director' column found in dataset!")

# --- 5. Word Cloud of Movie Titles ---
st.subheader("5. Word Cloud of Movie Titles")
movie_titles = " ".join(filtered[filtered['type'] == "Movie"]['title'].astype(str))
if movie_titles.strip():
    wordcloud = WordCloud(width=1100, height=400, background_color='black', colormap='autumn').generate(movie_titles)
    fig6, ax6 = plt.subplots(figsize=(15, 6))
    ax6.imshow(wordcloud, interpolation='bilinear')
    ax6.set_axis_off()
    st.pyplot(fig6)
    plt.clf()
else:
    st.info("No movie titles match the current filters for Word Cloud.")

# --- 6. Top 10 Countries Producing Content ---
st.subheader("6. Top 10 Countries Producing Content")
country_counts = filtered['country'].value_counts()
fig7, ax7 = plt.subplots(figsize=(10,6))
sns.barplot(x=country_counts.head(10).values, y=country_counts.head(10).index, palette="viridis", ax=ax7)
ax7.set_title("Top 10 Countries (Bar Chart)", fontsize=14, color="#e50914")
for i, v in enumerate(country_counts.head(10).values):
    ax7.text(v + 0.5, i, str(v), va='center', color="#e50914", fontweight='bold')
st.pyplot(fig7)
plt.clf()
pie_top5_other(country_counts, "Top 5 Countries (Pie Chart)")

# --- 7. Ratings Distribution ---
st.subheader("7. Ratings Distribution")
if "rating" in filtered.columns:
    r_counts = filtered['rating'].value_counts()
    fig8, ax8 = plt.subplots(figsize=(10,5))
    sns.barplot(x=r_counts.head(10).index, y=r_counts.head(10).values, palette="crest", ax=ax8)
    ax8.set_title("Ratings Distribution (Bar Chart)", fontsize=14, color="#e50914")
    ax8.set_xlabel("Rating")
    ax8.set_ylabel("Number of Titles")
    ax8.tick_params(axis='x', rotation=45)
    for i, v in enumerate(r_counts.head(10).values):
        ax8.text(i, v + 0.5, str(v), ha='center', color="#e50914", fontweight='bold')
    st.pyplot(fig8)
    plt.clf()
    pie_top5_other(r_counts, "Top 5 Ratings (Pie Chart)")
else:
    st.info("No 'rating' column found for Ratings Distribution.")

st.success("All charts update live as you use the sidebar filters. Enjoy exploring Netflix data!")
