import streamlit as st
import pickle
import pandas as pd

import os
import gdown

# Google Drive file ID
file_id = "1jvkQb2M-CEfvIIFZoKqK-1yMR5Rm6T4x" 
url = f"https://drive.google.com/uc?id={file_id}"
output = "similarity.pkl"

# checking part
if not os.path.exists(output):
    gdown.download(url, output, quiet=False)

# Load pickled data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommend function
def recommend(movie):
    movie = movie.lower()
    if movie not in movies['title'].str.lower().values:
        return ["Movie not found. Check spelling or try another!"]
    
    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movie_list = sorted(distances, reverse=True, key=lambda x: x[1])[1:6]
    
    return [movies.iloc[i[0]].title for i in movie_list]

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="centered")
st.title("Movie Recommender System")


selected_movie = st.selectbox(
    "Type or select a movie from the dropdown:",
    movies['title'].sort_values()
)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    st.subheader("Top 5 Recommendations:")
    for i, rec in enumerate(recommendations, start=1):
        st.write(f"{i}. {rec}")
