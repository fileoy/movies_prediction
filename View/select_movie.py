import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
import requests

API_URL = "https://movies-prediction.onrender.com/predict"
df = pd.read_csv('data_with_cluster.csv')
df.drop(columns="Unnamed: 0", inplace=True)


genre_columns = [
    'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
    'Documentary', 'Drama', 'Family', 'Fantasy', 'Film_Noir', 'History',
    'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Romance', 'Sci_Fi',
    'Sport', 'Thriller', 'Unknown', 'War', 'Western'
]

st.title("Movie Cluster Predictor")

selected_genres = st.multiselect("Select genres:", genre_columns)



user_genres = {genre: 1 if genre in selected_genres else 0 for genre in genre_columns}


if st.button("Predict Cluster"):
    if any(user_genres):
        
        response = requests.post(API_URL, json=user_genres)

        if response.status_code == 200:
            prediction = response.json()["pred"]
            st.write(f"The prediction is: {prediction}")
        else:
            st.error("Error making prediction!") 
          
        
        #recommended = df[df['Cluster'] == prediction(user_genres)]
        
        if st.checkbox("Show recomended movies"):
            st.dataframe(recommended[['Title','Rating','Number of User Reviews','Genres','Cluster']])
    else:
        st.error("Please select at least one genre.")
        
        
        
