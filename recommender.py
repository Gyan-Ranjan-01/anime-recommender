import os, re
import numpy as np
import pandas as pd
import faiss
import torch
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import MinMaxScaler
from rapidfuzz import fuzz, process

#defining path
EMBEDDING_PATH = 'final_embedding.npy'
INDEX_PATH = 'anime.index'

#configuring device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

numeric_cols = ['Score', 'Episodes', 'Rank', 'Popularity', 'Favorites', 'Scored By']

#function to load data
def load_data():
    data = pd.read_csv('anime-dataset-2023.csv')
    data.drop(columns=['anime_id', 'Aired', 'Premiered', 'Status',
                        'Image URL', 'Producers', 'Licensors'], inplace=True)
    data['English name'] = data['English name'].str.replace('\xa0', '', regex=False).str.strip()
    data['Other name'] = data['Other name'].fillna('')
    data['Other name'] = data['Other name'].str.replace('UNKNOWN', '',regex = False)
    data = data.drop_duplicates(subset='English name', keep='first').reset_index(drop=True)
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    return data


def build_index(data):
    scaler = MinMaxScaler()
    data_t = data[['Genres','Synopsis','Type','Studios','Source','Rating']].fillna(' ').copy()
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())
    data_n = scaler.fit_transform(data[numeric_cols])

    data_t['text'] = (
        data_t['Genres'].str.replace(',', ' ', regex=False) + ' ' +
        data_t['Synopsis'] + ' ' + data_t['Type'] + ' ' +
        data_t['Studios'] + ' ' + data_t['Source'] + ' ' + data_t['Rating']
    )

    model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
    movie_embedding = model.encode(data_t['text'].tolist(),
                                   convert_to_numpy=True, show_progress_bar=True)

    data_n = np.ascontiguousarray(data_n.astype(np.float32))
    movie_embedding = np.ascontiguousarray(movie_embedding.astype(np.float32))
    faiss.normalize_L2(movie_embedding)
    faiss.normalize_L2(data_n)

    final_embedding = np.hstack([movie_embedding * 0.4, data_n * 0.6]).astype(np.float32)
    faiss.normalize_L2(final_embedding)

    index = faiss.IndexFlatIP(final_embedding.shape[1])
    index.add(final_embedding)

    np.save(EMBEDDING_PATH, final_embedding)
    faiss.write_index(index, INDEX_PATH)
    return final_embedding, index

# load the data
data = load_data()

#try to fetch the cache files else running the build index function
try:
    final_embedding = np.load(EMBEDDING_PATH)
    index = faiss.read_index(INDEX_PATH)
    print("Loaded from cache")
except FileNotFoundError:
    print("Cache not found, recomputing...")
    final_embedding, index = build_index(data)
    print("Saved to cache")

#search list for fuzz_match_title function
data['search_text'] = (data['Name'].fillna('') + ' ' +
                       data['English name'].fillna('') + ' ' +
                       data['Other name'].fillna(''))


d_title = data['search_text'].tolist()


def fuzz_match_title(user_inp, threshold=60):
    result = process.extractOne(
        user_inp.strip().lower(),
        [t.lower() for t in d_title],
        scorer=fuzz.WRatio,
        score_cutoff=threshold
    )
    if result is None:
        return None
    _, _, idx = result
    return idx


def recommend(user_inp, k=5):
    idx = fuzz_match_title(user_inp)
    if idx is None:
        return None, []

    query_name = data['English name'][idx]
    base_name = re.split(r'[\s:]*(2|II|\(|\:)', query_name)[0].strip().lower()

    query_vec = final_embedding[idx].reshape(1, -1).astype(np.float32)
    faiss.normalize_L2(query_vec)
    S, I = index.search(query_vec, k + 20)

    seen, results = set(), []
    for i in range(1, len(I[0])):
        cidx = I[0][i]
        cname = data.iloc[cidx]['English name'].lower()
        cbase = re.split(r'[\s:]*(2|II|\(|\:)', cname)[0].strip()
        if cbase == base_name or cbase in seen:
            continue
        seen.add(cbase)
        results.append({
            "title": data.iloc[cidx]['English name'],
            "other_name": data.iloc[cidx]['Other name'],
            "score": round(float(S[0][i]), 4)
        })
        if len(results) == k:
            break

    return query_name, results