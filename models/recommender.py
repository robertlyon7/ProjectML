import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentRecommender:
    def __init__(self):
        self.df = pd.read_csv("data/movies.csv")

        self.df['combined_features'] = self.df['genres'].fillna('') + ' ' + self.df['overview'].fillna('')

        vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = vectorizer.fit_transform(self.df['combined_features'])

        self.similarity = cosine_similarity(self.tfidf_matrix)

    def recommend(self, movie_title, top_n=10):
        if movie_title not in self.df['title'].values:
            return []
        idx = self.df[self.df['title'] == movie_title].index[0]
        sim_scores = list(enumerate(self.similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]
        movie_indices = [i[0] for i in sim_scores]
        recommended_movies = []
        for i in movie_indices:
            movie = self.df.iloc[i]
            recommended_movies.append({
                "title": movie['title'],
                "overview": movie['overview'],
                "poster_path": movie['poster_path'],
                "vote_average": movie['vote_average']
            })
        return recommended_movies
