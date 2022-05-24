import streamlit as st
import pickle
import pandas as pd
import requests

page_bg_img = '''
<style>
body {
  background-image: url('https://getreelcinemas.com//wp-content/uploads/2015/02/Background-Narrow.jpg');
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=c21b44e59d3ad4bd7a96bb56713ec811&language=en-US'.format(
            movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/original/' + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    likeness = similarity[movie_index]
    movies_list = sorted(list(enumerate(likeness)), reverse=True, key=lambda x: x[1])[1:number_of_movies+2]

    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch_poster
        recommend_movies_poster.append(fetch_poster(movie_id))
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies, recommend_movies_poster


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Which movie do you like the Most?',
    movies['title'].values
)

number_of_movies = st.selectbox(
    'How many would you like to get recommended?',
    range(5, 11, 1)
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col = st.columns(5)
    for i in range(number_of_movies):
        with col[i % 5]:
            st.text(names[i + 1])
            st.image(posters[i + 1])
