from flask import Flask, render_template, request, abort
from models.recommender import ContentRecommender
import os
import random
import json

app = Flask(__name__)
recommender = ContentRecommender()


@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = ""
    selected_genre = ""
    selected_movie = None
    filtered_df = recommender.df.copy()

    if request.method == 'POST':
        search_query = request.form.get('search', '').strip().lower()
        selected_genre = request.form.get('genre', '')
        selected_movie = request.form.get('movie', '')
        surprise = request.form.get('surprise', '')

        if search_query:
            filtered_df = filtered_df[filtered_df['title'].str.lower(
            ).str.contains(search_query)]

        if selected_genre:
            filtered_df = filtered_df[filtered_df['genres'].str.contains(
                selected_genre, case=False, na=False)]

        if surprise: 
            selected_movie = random.choice(filtered_df['title'].tolist())

        recommendations = recommender.recommend(
            selected_movie) if selected_movie else []
    else:
        recommendations = []

    available_movies = sorted(filtered_df['title'].tolist())

    return render_template(
        'index.html',
        movies=available_movies,
        selected=selected_movie,
        recommendations=recommendations,
        all_titles=json.dumps(recommender.df['title'].dropna().tolist())
    )


@app.route('/movie/<title>')
def movie_detail(title):
    movie = recommender.df[recommender.df['title'] == title]
    if movie.empty:
        abort(404)
    movie = movie.iloc[0]
    return render_template(
        'movie_detail.html',
        title=movie['title'],
        overview=movie['overview'],
        poster_path=movie['poster_path'],
        vote_average=movie['vote_average'],
        genres=movie['genres']
    )


if __name__ == '__main__':
    app.run(debug=True)
