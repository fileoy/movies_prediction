import streamlit as st
import pandas as pd
import requests

API_URL = "https://movies-prediction.onrender.com/predict"
df = pd.read_csv('data_with_cluster.csv')
df.drop(columns="Unnamed: 0", inplace=True)

# Define genres
genre_columns = [
    'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
    'Documentary', 'Drama', 'Family', 'Fantasy', 'Film_Noir', 'History',
    'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Romance', 'Sci_Fi',
    'Sport', 'Thriller', 'Unknown', 'War', 'Western'
]

st.title("Movie Cluster Predictor")

# User selects genres
selected_genres = st.multiselect("Select genres:", genre_columns)

# Convert selected genres into a dictionary
user_genres = {genre: 1 if genre in selected_genres else 0 for genre in genre_columns}

if st.button("Predict Cluster"):
    if any(user_genres.values()):  # Ensure at least one genre is selected
        try:
            # Send request to the API
            response = requests.post(API_URL, json=user_genres)
            if response.status_code == 200:
                prediction = response.json()["pred"]
                st.write(f"The predicted cluster is: {prediction}")

                # Filter the DataFrame for recommendations
                recommended = df[df['Cluster'] == prediction]
                if not recommended.empty:
                    st.write("Recommended Movies:")
                    st.dataframe(recommended[['Title', 'Rating', 'Number of User Reviews', 'Genres']])
                else:
                    st.write("No recommendations found for this cluster.")
            else:
                st.error("Error: Unable to fetch prediction from the API.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please select at least one genre.")
