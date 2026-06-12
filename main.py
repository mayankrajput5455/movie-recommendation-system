import os
import pickle
from typing import Optional, List, Dict, Any, Tuple

import numpy as np
import pandas as pd
import httpx

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# =========================
# ENV
# =========================
load_dotenv()


OMDB_API_KEY = os.getenv("OMDB_API_KEY")
print("OMDB KEY:", OMDB_API_KEY)
OMDB_BASE = "https://www.omdbapi.com"

if not OMDB_API_KEY:
    raise RuntimeError(
        "OMDB_API_KEY missing. Put it in .env as OMDB_API_KEY=xxxx"
    )

# =========================
# FASTAPI
# =========================
app = FastAPI(
    title="Movie Recommender API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# FILES
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DF_PATH = os.path.join(BASE_DIR, "df.pkl")
INDICES_PATH = os.path.join(BASE_DIR, "indices.pkl")
TFIDF_MATRIX_PATH = os.path.join(BASE_DIR, "tfidf_matrix.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "tfidf.pkl")

df = None
indices_obj = None
tfidf_matrix = None
tfidf_obj = None

TITLE_TO_IDX = None

# =========================
# MODELS
# =========================
class MovieCard(BaseModel):
    imdb_id: str
    title: str
    poster_url: Optional[str] = None
    year: Optional[str] = None


class MovieDetails(BaseModel):
    imdb_id: str
    title: str
    overview: Optional[str] = None
    year: Optional[str] = None
    poster_url: Optional[str] = None
    genres: List[str] = []
    imdb_rating: Optional[str] = None


class TFIDFRecItem(BaseModel):
    title: str
    score: float
    movie: Optional[MovieCard] = None


class SearchBundleResponse(BaseModel):
    query: str
    movie_details: MovieDetails
    recommendations: List[TFIDFRecItem]

# =========================
# HELPERS
# =========================
def normalize_title(title):
    return str(title).strip().lower()


def build_title_map(indices):
    mapping = {}

    if isinstance(indices, dict):
        for k, v in indices.items():
            mapping[normalize_title(k)] = int(v)
        return mapping

    for k, v in indices.items():
        mapping[normalize_title(k)] = int(v)

    return mapping


async def omdb_get(params):

    params["apikey"] = OMDB_API_KEY

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(
            OMDB_BASE,
            params=params
        )

    data = response.json()

    if data.get("Response") == "False":
        raise HTTPException(
            status_code=404,
            detail=data.get("Error")
        )

    return data


async def omdb_search_movies(query):

    return await omdb_get(
        {
            "s": query,
            "type": "movie"
        }
    )


async def omdb_movie_details(imdb_id):

    data = await omdb_get(
        {
            "i": imdb_id,
            "plot": "full"
        }
    )

    return MovieDetails(
        imdb_id=data["imdbID"],
        title=data["Title"],
        overview=data.get("Plot"),
        year=data.get("Year"),
        poster_url=data.get("Poster"),
        genres=data.get("Genre", "").split(", "),
        imdb_rating=data.get("imdbRating")
    )


async def attach_movie_card(title):

    try:
        data = await omdb_search_movies(title)

        movies = data.get("Search", [])

        if not movies:
            return None

        movie = movies[0]

        return MovieCard(
            imdb_id=movie["imdbID"],
            title=movie["Title"],
            poster_url=movie["Poster"],
            year=movie["Year"]
        )

    except:
        return None

# =========================
# TF-IDF
# =========================
def get_idx(title):

    key = normalize_title(title)

    if key not in TITLE_TO_IDX:
        raise HTTPException(
            status_code=404,
            detail=f"Movie not found in dataset: {title}"
        )

    return TITLE_TO_IDX[key]


def tfidf_recommend(title, top_n=10):

    idx = get_idx(title)

    qv = tfidf_matrix[idx]

    scores = (tfidf_matrix @ qv.T).toarray().ravel()

    order = np.argsort(-scores)

    results = []

    for i in order:

        if i == idx:
            continue

        movie_title = str(df.iloc[i]["title"])

        results.append(
            (
                movie_title,
                float(scores[i])
            )
        )

        if len(results) >= top_n:
            break

    return results

# =========================
# STARTUP
# =========================
@app.on_event("startup")
def startup():

    global df
    global indices_obj
    global tfidf_matrix
    global tfidf_obj
    global TITLE_TO_IDX

    with open(DF_PATH, "rb") as f:
        df = pickle.load(f)

    with open(INDICES_PATH, "rb") as f:
        indices_obj = pickle.load(f)

    with open(TFIDF_MATRIX_PATH, "rb") as f:
        tfidf_matrix = pickle.load(f)

    with open(TFIDF_PATH, "rb") as f:
        tfidf_obj = pickle.load(f)

    TITLE_TO_IDX = build_title_map(indices_obj)

# =========================
# ROUTES
# =========================
@app.get("/")
def root():
    return {
        "message": "Movie Recommendation API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/search")
async def search_movies(
    query: str
):
    return await omdb_search_movies(query)


@app.get(
    "/movie/{imdb_id}",
    response_model=MovieDetails
)
async def movie_details(
    imdb_id: str
):
    return await omdb_movie_details(imdb_id)


@app.get("/recommend")
async def recommend(
    title: str = Query(...),
    top_n: int = Query(10)
):

    recs = tfidf_recommend(
        title,
        top_n
    )

    output = []

    for movie_title, score in recs:

        card = await attach_movie_card(movie_title)

        output.append(
            {
                "title": movie_title,
                "score": score,
                "movie": card
            }
        )

    return output


@app.get(
    "/movie/search",
    response_model=SearchBundleResponse
)
async def movie_search(
    query: str,
    top_n: int = 10
):

    search_result = await omdb_search_movies(query)

    movies = search_result.get("Search", [])

    if not movies:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    imdb_id = movies[0]["imdbID"]

    details = await omdb_movie_details(
        imdb_id
    )

    try:
        recs = tfidf_recommend(
            details.title,
            top_n
        )
    except:
        recs = []

    recommendation_list = []

    for title, score in recs:

        card = await attach_movie_card(
            title
        )

        recommendation_list.append(
            TFIDFRecItem(
                title=title,
                score=score,
                movie=card
            )
        )

    return SearchBundleResponse(
        query=query,
        movie_details=details,
        recommendations=recommendation_list
    )
