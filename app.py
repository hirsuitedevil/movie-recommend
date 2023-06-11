import pandas as pd
import streamlit as st
import pickle
import requests

st.title('Movie Recommendation System')


def get_single_poster_filepath(data):
    posters = data.get('posters', [])
    if posters:
        return posters[0]['file_path']
    return None


def get_poster(movie_id):
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlYzMwMjliYjQ2OTQwNTJhY2RiYWQzNTE3NWQyM2ZlOSIsInN1YiI6IjY0ODMwMWU5YmYzMWYyNTA1NjlhYjRkYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1_-EpuJDzNLiw-QZNhRbUZjrKkz_3aYPwgmKNHAT598"
    }

    response = requests.get('https://api.themoviedb.org/3/movie/{}/images?include_image_language=en'.format(movie_id), headers=headers)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+get_single_poster_filepath(data)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(get_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox('Select movie', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    i = 0
    col1,  col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    for col in cols:
        with col:
            st.caption(names[i])
            st.image(posters[i])
            i += 1
