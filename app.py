import streamlit as st
import pickle
import requests
import pandas as pd
from pathlib import Path

# --- Helper to load pickle safely ---
BASE_DIR = Path(__file__).resolve().parent

def load_pickle(filename):
    p = BASE_DIR / filename
    try:
        with p.open('rb') as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"❌ Error loading {filename}: {e}")
        st.stop()

# --- Fetch movie poster from TMDB ---
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

# --- Recommendation function ---
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []

        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]]['id']
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]]['title'])

        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error in recommendation: {e}")
        return [], []

# --- Load data ---
movies = load_pickle('movie_list.pkl')      # 🔥 changed here
similarity = load_pickle('similarity.pkl')  # 🔥 changed here

# Ensure movies is DataFrame
if not isinstance(movies, pd.DataFrame):
    movies = pd.DataFrame(movies)

st.success("✅ Data loaded successfully!")

# --- Streamlit UI ---
st.header('🎬 Movie Recommender System')

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    with st.spinner('Finding similar movies...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names:
        st.success(f"🎯 Recommendations for: **{selected_movie}**")

        cols = st.columns(5)
        for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                st.image(poster, use_container_width=True)
                st.markdown(f"**{name}**")
    else:
        st.warning("No recommendations found. Please try a different movie.")

# Footer
st.markdown("---")
st.markdown("💡 *Select a movie and click 'Show Recommendation' to discover similar movies*")
