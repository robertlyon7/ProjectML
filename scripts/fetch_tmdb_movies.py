import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
    
GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
}

def fetch_movies(pages=5):
    all_movies = []
    for page in range(1, pages + 1):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Error fetching page {page}: {res.status_code}")
            continue

        for movie in res.json().get("results", []):
            genres = [GENRE_MAP.get(genre_id, str(genre_id)) for genre_id in movie.get("genre_ids", [])]
            all_movies.append({
                "title": movie.get("title", ""),
                "overview": movie.get("overview", ""),
                "genres": ", ".join(genres),
                "keywords": movie.get("title", ""),  
                "popularity": movie.get("popularity", 0.0),
                "vote_average": movie.get("vote_average", 0.0),
                "poster_path": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}"
            })

    df = pd.DataFrame(all_movies)
    df.to_csv("data/movies.csv", index=False)
    print(f"✅ Saved {len(df)} movies to data/movies.csv")

if __name__ == "__main__":
    fetch_movies(pages=10)
