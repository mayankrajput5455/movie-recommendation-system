# 🎬 AI-Powered Movie Recommendation System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36.0-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.7.2-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7.svg?logo=render&logoColor=white)](https://movie-recommendation-system-c8g5.onrender.com)

A full-stack, content-based **Movie Recommendation System** powered by Machine Learning (TF-IDF Vectorization & Cosine Similarity), a **FastAPI** backend, and an interactive **Streamlit** dark-themed web application. Enriched with real-time movie posters, plots, and IMDb ratings via the **OMDb API**.

---

## 🌟 Live Demo

- **Backend API Base URL:** `https://movie-recommendation-system-c8g5.onrender.com`
- **Interactive API Docs (Swagger UI):** `https://movie-recommendation-system-c8g5.onrender.com/docs`

---

## 📌 Features

- **🎯 Content-Based Recommendations:** Generates top $N$ movie recommendations based on textual similarity (plots, overviews, genres) using pre-calculated **TF-IDF matrices** and **Cosine Similarity**.
- **🔍 Instant Search & Auto-complete:** Live movie title search powered by OMDb API.
- **🖼️ Rich Media & Metadata:** Displays high-resolution movie posters, release years, IMDb ratings, genres, and full plot summaries.
- **🚀 High Performance API:** Asynchronous FastAPI backend built with `httpx` and `pydantic` schemas for rapid response times.
- **🎨 Sleek Modern UI:** Fully customized Streamlit dashboard with responsive movie card grids, dark mode aesthetics, and smooth loading spinners.

---

## 🏗️ Architecture & Tech Stack

```
   ┌───────────────────────┐
   │ Streamlit Frontend    │ (app.py)
   │ (Interactive Web UI)  │
   └───────────┬───────────┘
               │ HTTP Requests (REST)
               ▼
   ┌───────────────────────┐
   │ FastAPI Backend       │ (main.py)
   │ (REST API & CORS)     │
   └─────┬───────────┬─────┘
         │           │
         │ TF-IDF    │ Live Search & Posters
         ▼           ▼
   ┌───────────┐ ┌───────────────┐
   │ Scikit    │ │ OMDb API      │
   │ Learn ML  │ │ (External API)│
   └───────────┘ └───────────────┘
```

### **Technologies Used**
- **Machine Learning & Data Processing:** Python, Pandas, NumPy, Scikit-Learn (TF-IDF, Cosine Similarity), SciPy, Pickle
- **Backend Framework:** FastAPI, Uvicorn, Pydantic, HTTPX, Python-Dotenv
- **Frontend Framework:** Streamlit, Custom CSS / HTML Injection
- **External Services:** OMDb (Open Movie Database API)
- **Deployment:** Render (Backend API)

---

## 📂 Repository Structure

```text
├── app.py                  # Streamlit web application interface
├── main.py                 # FastAPI backend server with ML inference & OMDb integration
├── movies.ipynb            # Jupyter Notebook for data cleaning, EDA, & TF-IDF model training
├── movies_metadata.csv     # Raw dataset containing movie metadata
├── df.pkl                  # Processed DataFrame pickle file
├── indices.pkl             # Movie title to index mapping dictionary
├── tfidf.pkl               # Trained TF-IDF Vectorizer model
├── tfidf_matrix.pkl        # Pre-computed sparse TF-IDF matrix
├── requirements.txt        # Python package dependencies
├── runtime.txt             # Deployment Python runtime specification
└── .env                    # Environment variables (OMDb API key)
```

---

## 🚀 Getting Started (Local Setup)

### **1. Prerequisites**
Ensure you have **Python 3.10+** installed on your system.

### **2. Clone the Repository**
```bash
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system
```

### **3. Create a Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5. Configure Environment Variables**
Create a `.env` file in the root directory and add your free **OMDb API Key** (Get one at [omdbapi.com](https://www.omdbapi.com/apikey.aspx)):

```env
OMDB_API_KEY=your_omdb_api_key_here
```

---

## 💻 Running the Application

### **Option 1: Run Backend API First (Recommended)**

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
2. Open `http://127.0.0.1:8000/docs` in your browser to view the interactive API documentation.

3. Update `API_BASE` in `app.py` if running locally:
   ```python
   API_BASE = "http://127.0.0.1:8000"
   ```

4. Launch the Streamlit Frontend (in a new terminal):
   ```bash
   streamlit run app.py
   ```

---

## 📡 API Endpoints Reference

| Endpoint | Method | Description | Parameters |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | API status message | None |
| `/health` | `GET` | Health check endpoint | None |
| `/search` | `GET` | Search movies from OMDb | `query` (str) |
| `/movie/{imdb_id}` | `GET` | Get full movie details & poster | `imdb_id` (str) |
| `/recommend` | `GET` | Get top content-based recommendations | `title` (str), `top_n` (int) |
| `/movie/search` | `GET` | Combined search + details + recommendations | `query` (str), `top_n` (int) |

---

## 🧠 Machine Learning Model Details

1. **Preprocessing:** Text data (overviews, descriptions, genres) are cleaned, normalized, and preprocessed in `movies.ipynb`.
2. **Feature Extraction:** `TfidfVectorizer` converts textual descriptions into a numerical sparse feature matrix.
3. **Similarity Calculation:** When a user selects a movie, cosine similarity scores are calculated between the target vector and all matrix vectors:
   $$\text{Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$
4. **Ranking:** Results are sorted in descending order of similarity score to return the top recommendations.

---

## 👤 Author

Developed by **Mayank Singh**  
- **GitHub:** [@mayankrajput5455](https://github.com/mayankrajput5455)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
