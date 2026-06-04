# 🎌 Anime Recommender System

A high-performance, ML-powered anime recommendation engine using semantic search and vector similarity. Built with Sentence Transformers, FAISS, and FastAPI — deployed on Hugging Face Spaces via Docker.

## 🚀 Live Demo

🔗 [Try it on Hugging Face Spaces](https://huggingface.co/spaces/gyan-ranjan/anime-recommender)

## 🧠 How It Works

The system separates the heavy ML work (done once, offline) from the lightweight runtime (fast API inference):

1. **Offline — Embedding Generation** (`notebooks/Model.ipynb`): The `all-MiniLM-L6-v2` transformer encodes text features (synopsis, genres, studios) into dense vectors. Numeric features (score, popularity, rank) are normalized via `MinMaxScaler` and concatenated into a unified feature space. The resulting FAISS index and embeddings are cached to disk.

2. **Runtime — API Inference** (`recommender.py`): The FastAPI backend loads the pre-computed FAISS index directly — no neural network at runtime. Achieves O(log N) search complexity with full semantic accuracy.

3. **Fuzzy Matching** (`recommender.py`): User input is cleaned via `RapidFuzz` (WRatio scorer) to handle typos and partial titles before the vector search executes.

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | FastAPI, Python |
| **ML / NLP** | PyTorch, Sentence-Transformers (`all-MiniLM-L6-v2`) |
| **Vector Search** | FAISS (IndexFlatIP) |
| **String Matching** | RapidFuzz |
| **Data Processing** | Pandas, NumPy, Scikit-Learn |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Deployment** | Docker, Hugging Face Spaces |

## 📂 Project Structure

```text
├── Notebooks/
│   └── Model.ipynb          # Offline embedding generation pipeline
├── static/
│   ├── script.js            # Async API calls and UI updates
│   └── style.css            # Dark-theme responsive styling
├── templates/
│   └── index.html           # Jinja2 frontend template
├── app.py                   # FastAPI routing
├── recommender.py           # FAISS indexing and vector search logic
├── Dockerfile               # Production container config
├── requirements.txt         # Dependencies
├── anime-dataset-2023.csv   # Raw dataset
├── anime.index              # Pre-computed FAISS index (cached)
└── final_embedding.npy      # Serialized embeddings (cached)
```

## 🏃 Run Locally

```bash
# Clone the repo
git clone https://github.com/Gyan-Ranjan-01/anime-recommender.git
cd anime-recommender

# Install dependencies
pip install -r requirements.txt

# Generate embeddings (first time only — requires GPU recommended)
jupyter notebook Notebooks/Model.ipynb

# Start the API
uvicorn app:app --reload
```

Then open `http://localhost:8000` in your browser.

> **Note:** `anime.index` and `final_embedding.npy` are pre-generated artifacts. If not present, run the notebook first to generate them.

## 📊 Dataset

[Anime Dataset 2023 — Kaggle](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset)

## 👨‍💻 Author

**Gyan Ranjan**
Information Technology, IIEST Shibpur

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gyan-ranjan-/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Gyan-Ranjan-01)