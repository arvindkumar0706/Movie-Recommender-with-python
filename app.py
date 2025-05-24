from flask import Flask, render_template, request
from recommendation import get_recommendations
import requests

app = Flask(__name__)

# 🔑 Replace this with your OMDb API key
OMDB_API_KEY = "aedad2d2"  

def get_poster_url(title):
    import requests
    query = title.replace(" ", "+")
    url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API_KEY}"
    print(f"Fetching URL: {url}")  # Debug print
    try:
        response = requests.get(url)
        data = response.json()
        print("OMDb Response:", data)  # Debug print
        if data.get("Response") == "True" and data.get("Poster") != "N/A":
            return data.get("Poster")
    except Exception as e:
        print("Error fetching poster:", e)
    return "https://via.placeholder.com/300x450?text=No+Image"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form['movie']
    recommended_titles = get_recommendations(movie)

    results = []
    for title in recommended_titles:
        poster = get_poster_url(title)
        results.append({"title": title, "poster": poster})

    print(f"Movie input: {movie}")
    print(f"Recommendations: {recommended_titles}")
    return render_template('recommend.html', movie=movie, recommendations=results)

if __name__ == '__main__':
    app.run(debug=True)
