import requests
import streamlit as st

API_BASE = "https://movie-recommendation-system-c8g5.onrender.com"
# API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# =====================================
# CSS
# =====================================
st.markdown("""
<style>

.hero {
    text-align: center;
    padding: 1rem 0;
}

.hero h1 {
    font-size: 3rem;
}

.hero p {
    color: #9ca3af;
}

.movie-card {
    background: #1a1d24;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    height: 90px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-top: 12px;
    margin-bottom: 12px;
}


.movie-title {
    font-weight: 600;
    height: 45px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}


.score {
    color: #facc15;
    font-weight: bold;
}

[data-testid="stImage"] img {
    width: 100% !important;
    height: 400px !important;
    object-fit: cover !important;
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# API HELPER
# =====================================
def api_get(path, params=None):
    try:
        response = requests.get(
            f"{API_BASE}{path}",
            params=params,
            timeout=30
        )

        if response.status_code != 200:
            st.error(response.text)
            return None

        return response.json()

    except Exception as e:
        st.error(str(e))
        return None


# =====================================
# HEADER
# =====================================
st.markdown("""
<div class="hero">
    <h1>🎬 Movie Recommendation System</h1>
    <p>Discover movies you'll love using AI-powered recommendations</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# =====================================
# SEARCH
# =====================================
query = st.text_input(
    "",
    placeholder="🔍 Search for a movie..."
)

if query:

    with st.spinner("Searching movies..."):
        search_results = api_get(
            "/search",
            {"query": query}
        )

    if search_results:

        movies = search_results.get("Search", [])

        if not movies:
            st.warning("No movies found.")
            st.stop()

        movie_options = {
            f"{m['Title']} ({m['Year']})": m["imdbID"]
            for m in movies
        }

        selected_movie = st.selectbox(
            "Select a movie",
            list(movie_options.keys())
        )

        imdb_id = movie_options[selected_movie]

        with st.spinner("Loading movie details..."):
            details = api_get(
                f"/movie/{imdb_id}"
            )

        if details:

            st.divider()

            poster_col, info_col = st.columns([1, 2])

            with poster_col:

                poster = details.get("poster_url")

                if poster and poster != "N/A":
                    st.image(
                        poster,
                        width=250
                    )

            with info_col:

                st.markdown(
                    f"# {details['title']}"
                )

                metric1, metric2, metric3 = st.columns(3)

                metric1.metric(
                    "IMDb Rating",
                    details.get("imdb_rating", "N/A")
                )

                metric2.metric(
                    "Year",
                    details.get("year", "N/A")
                )

                metric3.metric(
                    "Genres",
                    len(details.get("genres", []))
                )

                st.markdown(
                    f"**Genres:** {', '.join(details.get('genres', []))}"
                )

                st.markdown("### Overview")

                st.write(
                    details.get(
                        "overview",
                        "No overview available."
                    )
                )

            st.divider()

            # =====================================
            # RECOMMENDATIONS
            # =====================================
            st.subheader("🎯 Recommended Movies")

            with st.spinner("Generating recommendations..."):

                recommendations = api_get(
                    "/recommend",
                    {
                        "title": details["title"],
                        "top_n": 10
                    }
                )

            if recommendations:

                # Remove movies without posters
                recommendations = [
                    rec for rec in recommendations
                    if rec.get("movie")
                    and rec["movie"].get("poster_url")
                    and rec["movie"]["poster_url"] != "N/A"
                ]

                cols_per_row = 5

                for start in range(0, len(recommendations), cols_per_row):

                    row_movies = recommendations[start:start + cols_per_row]

                    # Create columns AFTER filtering
                    cols = st.columns(len(row_movies))

                    for col, rec in zip(cols, row_movies):

                        movie = rec["movie"]

                        with col:

                            st.markdown(
                                f"""
                                <div style="
                                    width:100%;
                                    height:420px;
                                    overflow:hidden;
                                    border-radius:12px;
                                    background:#111827;
                                    margin-bottom:8px;
                                ">
                                    <img
                                        src="{movie['poster_url']}"
                                        style="
                                            width:100%;
                                            height:100%;
                                            object-fit:cover;
                                        "
                                    />
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                f"""
                                <div class="movie-card">
                                    <div class="movie-title">
                                        {rec['title']}
                                    </div>
                                        <span>⭐ {rec['score']:.3f}</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

            else:
                st.warning(
                    "No recommendations available."
                )

            st.divider()

            _, center, _ = st.columns([1, 2, 1])

            with center:
                st.markdown("### 🎬 Movie Recommendation System")
                st.caption(
                    "Built with Streamlit • FastAPI • Scikit-Learn • OMDb API"
                )
                st.caption("Developed by Mayank Singh")
