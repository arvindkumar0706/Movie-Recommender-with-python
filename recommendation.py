import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv('movies.csv')

# Fill missing overviews
df['overview'] = df['overview'].fillna('')

# Create TF-IDF matrix based on movie overviews
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['overview'])

# Compute cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create a reverse map of indices and movie titles
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

def get_recommendations(title, num_recommendations=5):
    title = title.strip()
    if title not in indices:
        return []
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations+1]
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices].tolist()

import requests

OMDB_API_KEY = "http://www.omdbapi.com/?i=tt3896198&apikey=aedad2d2"  

def get_poster_url(movie_title):
    query = movie_title.replace(" ", "+")
    url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return data.get("Poster")
    else:
        return "https://via.placeholder.com/300x450?text=No+Image"