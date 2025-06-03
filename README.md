 Setup Instructions

1. Clone the repo
   git clone https://github.com/yourusername/movie-recommender.git
   cd movie-recommender

2. Install dependencies
   pip install -r requirements.txt

3. Set your TMDB API Key
   Replace the API key in `fetch_tmdb_movies.py`:
   API_KEY = 'YOUR_API_KEY_HERE'

4. Fetch Movie Data
   python fetch_tmdb_movies.py

5. Run the app
   python app.py
   
6. Open in browser:
   http://127.0.0.1:5000
