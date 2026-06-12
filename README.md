# 🎬 Movie Recommendation System

An AI-powered Movie Recommendation System built using **FastAPI**, **Streamlit**, **Scikit-Learn**, and the **OMDb API**. The application recommends similar movies using **TF-IDF Vectorization** and **Cosine Similarity** based on movie metadata.

## 🚀 Features

* 🔍 Search movies using OMDb API
* 🎬 View movie details including poster, genres, year, and IMDb rating
* 🤖 Get intelligent movie recommendations
* ⚡ FastAPI backend for recommendation serving
* 🎨 Interactive Streamlit frontend
* 📱 Responsive and user-friendly interface
* 🌐 Deployed on Render

---

## 🏗️ Tech Stack

### Frontend

* Streamlit

### Backend

* FastAPI
* Uvicorn

### Machine Learning

* Scikit-Learn
* TF-IDF Vectorization
* Cosine Similarity

### Data Processing

* Pandas
* NumPy

### External API

* OMDb API

---

## 📂 Project Structure

```bash
movie-recommendation-system/
│
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI backend
├── movies.pkl              # Movie dataset
├── tfidf.pkl               # TF-IDF vectorizer
├── tfidf_matrix.pkl        # TF-IDF matrix
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
OMDB_API_KEY=YOUR_OMDB_API_KEY
```

Get your free API key from:

https://www.omdbapi.com/apikey.aspx

---

## ▶️ Run Backend

```bash
uvicorn main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## ▶️ Run Frontend

```bash
streamlit run app.py
```

Frontend will run at:

```text
http://localhost:8501
```

---

## 🧠 Recommendation Engine

The recommendation system uses:

1. Movie metadata preprocessing
2. TF-IDF Vectorization
3. Cosine Similarity computation
4. Top-N similar movie retrieval

This content-based filtering approach recommends movies with similar themes and descriptions.

---

## 📸 Features Preview

* Movie Search
* Movie Details Page
* IMDb Ratings
* Genre Information
* Similar Movie Recommendations
* Poster Display

---

## 🌍 Deployment

### Backend

Deploy FastAPI on Render:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Frontend

Deploy Streamlit using:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## 📈 Future Improvements

* User authentication
* Collaborative filtering
* Hybrid recommendation system
* Movie trailers integration
* Watchlist feature
* Personalized recommendations

---

## 👨‍💻 Author

**Mayank Singh**

B.Tech (3rd Year) | Machine Learning & Full Stack Development Enthusiast

GitHub: https://github.com/mayankrajput5455

LinkedIn: Add Your LinkedIn Profile

---

## ⭐ Support

If you found this project useful, consider giving it a star on GitHub.
