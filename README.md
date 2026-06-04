---
title: Anime Recommender
emoji: 🎌
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
---

# 🎌 Anime Recommender System

A high-performance, machine learning-powered anime recommendation engine. This application leverages natural language processing to understand the thematic and narrative similarities between thousands of anime, delivering instant, highly accurate recommendations via a fast, modern web interface.

## 🚀 Live Demo

[gyan-ranjan/anime-recommender](https://huggingface.co/spaces/gyan-ranjan/anime-recommender)

## 🧠 Architecture & Optimization Strategy

To ensure blazing-fast response times in a production environment, this system strictly separates **heavy model generation** from **lightweight API inference**.

While the project utilizes robust ML libraries (`PyTorch`, `sentence-transformers`), they are intentionally isolated in the build pipeline to maximize runtime efficiency:

1. **Semantic Embedding Generation (Offline/Build Phase):** Using the `all-MiniLM-L6-v2` transformer model, the dataset's text features (synopsis, genres, studios) are encoded into dense high-dimensional vectors. Numeric features (score, popularity) are normalized via `scikit-learn` and concatenated to create a unified feature space.

2. **Production Inference (Online/Runtime Phase):** The FastAPI backend relies purely on a pre-computed `FAISS` (Facebook AI Similarity Search) index and `RapidFuzz`. By bypassing heavy neural network loading at runtime, the API achieves lightning-fast query speeds (O(log N) search complexity) while retaining deep semantic accuracy.

3. **Fuzzy Matching:** User inputs are sanitized and processed through `RapidFuzz` to correct typos and find the exact dataset match before executing the vector search.

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | FastAPI, Python |
| **ML / NLP** | PyTorch, Sentence-Transformers (Hugging Face) |
| **Vector Search** | FAISS |
| **String Matching** | RapidFuzz |
| **Data Processing** | Pandas, NumPy, Scikit-Learn |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Deployment** | Docker, Hugging Face Spaces |

## 📂 Project Structure

```text
├── static/
│   ├── script.js            # Handles async API calls and UI updates
│   └── style.css            # Modern, responsive dark-theme styling
├── templates/
│   └── index.html           # Jinja2 template for the frontend
├── app.py                   # FastAPI application routing
├── recommender.py           # Core logic: FAISS indexing and vector search
├── Dockerfile               # Production container configuration
├── requirements.txt         # Dependency management
├── anime-dataset.csv        # Raw tabular dataset
├── anime.index              # Pre-computed FAISS vector index (Cached)
└── final_embedding.npy      # Serialized NumPy embeddings (Cached)
```

## 👨‍💻 Author

**Gyan Ranjan**
Information Technology, IIEST Shibpur

Passionate about Full-Stack Development, AI/ML, and building high-performance, scalable systems.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gyan-ranjan-/)