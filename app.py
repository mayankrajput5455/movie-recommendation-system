import requests
import streamlit as st

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# --------------------------
# Helpers
# --------------------------
def api_get(path, params=None):
    try:
        r = requests.get(
            f"{API_BASE}{path}",
            params=params,
            timeout=30
        )

        if r.status_code != 200:
            st.error(r.text)
            return None

        return r.json()

    except Exception as e:
        st.error(str(e))
        return None


# --------------------------
# Header
# --------------------------
st.title("🎬 Movie Recommendation System")
st.caption("TF-IDF + OMDb")

# --------------------------
# Search
# --------------------------
query = st.text_input(
    "Search Movie",
    placeholder="Avatar"
)

if query:

    search_results = api_get(
        "/search",
        {"query": query}
    )

    if search_results:

        movies = search_results.get("Search", [])

        if movies:

            movie_options = {
                f"{m['Title']} ({m['Year']})": m["imdbID"]
                for m in movies
            }

            selected = st.selectbox(
                "Select Movie",
                list(movie_options.keys())
            )

            imdb_id = movie_options[selected]

            details = api_get(
                f"/movie/{imdb_id}"
            )

            if details:

                st.divider()

                col1, col2 = st.columns([1, 2])

                with col1:

                    if details["poster_url"] != "N/A":
                        st.image(
                            details["poster_url"],
                            use_container_width=True
                        )

                with col2:

                    st.subheader(details["title"])

                    st.write(
                        f"⭐ IMDb Rating: {details['imdb_rating']}"
                    )

                    st.write(
                        f"📅 Year: {details['year']}"
                    )

                    st.write(
                        f"🎭 Genres: {', '.join(details['genres'])}"
                    )

                    st.write(details["overview"])

                st.divider()

                st.subheader(
                    "Recommended Movies"
                )

                recommendations = api_get(
                    "/recommend",
                    {
                        "title": details["title"],
                        "top_n": 10
                    }
                )

                if recommendations:

                    cols = st.columns(5)

                    for idx, rec in enumerate(recommendations):

                        movie = rec.get("movie")

                        with cols[idx % 5]:

                            if (
                                movie
                                and movie["poster_url"]
                                and movie["poster_url"] != "N/A"
                            ):
                                st.image(
                                    movie["poster_url"],
                                    use_container_width=True
                                )

                            st.caption(
                                rec["title"]
                            )

                            st.write(
                                f"Score: {rec['score']:.3f}"
                            )

