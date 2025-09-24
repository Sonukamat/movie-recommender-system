import streamlit as st
import pickle
import requests
import pandas as pd


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    try:
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"


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


# Load data from local files
try:
    movies = pickle.load(open('model/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))
    st.success("✅ Data loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading files: {e}")
    st.stop()

# Ensure movies is a DataFrame
if not isinstance(movies, pd.DataFrame):
    movies = pd.DataFrame(movies)

# --- Streamlit UI ---
st.header('🎬 Movie Recommender System')

# Get movie list
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

        # Create columns for display
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.image(recommended_movie_posters[0], use_container_width=True)  # Fixed
            st.markdown(f"**{recommended_movie_names[0]}**")

        with col2:
            st.image(recommended_movie_posters[1], use_container_width=True)  # Fixed
            st.markdown(f"**{recommended_movie_names[1]}**")

        with col3:
            st.image(recommended_movie_posters[2], use_container_width=True)  # Fixed
            st.markdown(f"**{recommended_movie_names[2]}**")

        with col4:
            st.image(recommended_movie_posters[3], use_container_width=True)  # Fixed
            st.markdown(f"**{recommended_movie_names[3]}**")

        with col5:
            st.image(recommended_movie_posters[4], use_container_width=True)  # Fixed
            st.markdown(f"**{recommended_movie_names[4]}**")
    else:
        st.warning("No recommendations found. Please try a different movie.")

# Add some styling and information
st.markdown("---")
st.markdown("💡 *Select a movie and click 'Show Recommendation' to discover similar movies*")