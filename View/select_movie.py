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

# Define cluster descriptions
cluster_descriptions = {
    0: "Mostly Docu-mental Movies",
    1: "Laughs and Lessons Movies",
    2: "Love, Laughter, and Tears Movies",
    3: "Teenagers Movies",
    4: "Guns & Fighting Movies",
    5: "Drama Movies",
    6: "Jump Scares Movies",
    7: "Family Friendly Movies"
}

st.title("🎥 Movie Recommendation 🍿")

# Funny description
st.write(
    """
    Welcome to Movie Predictor using
    
    **AI**
    
    **MACHINE LEARNING**
    
    **BIG DATA**
    
    **AND MORE...**
    
    we give you  **THE ULTIMATE MOVIE RECOMMENDATION SYSTEM!** 🚀
    
    A simple and fun movie recommendation site.  
    
    Choose your favorite genres (up to 5, don't be greedy!), and we'll find your movie type for you.  
    🎬 Let's make your next movie night legendary! 🌟
    """
)

# User selects genres with validation for a maximum of 5 selections
selected_genres = st.multiselect("Select genres (Max 5):", genre_columns)

if len(selected_genres) > 5:
    st.error("🚫 Whoa there! You can't have everything. Pick only 5 genres, please!")

# Convert selected genres into a dictionary
user_genres = {genre: 1 if genre in selected_genres else 0 for genre in genre_columns}

if st.button("Discover Movies!"):
    if len(selected_genres) == 0:
        st.error("❌ Oops! You need to select at least one genre. Don't be shy, make a choice!")
    elif len(selected_genres) > 5:
        st.error("🚫 Too many genres! Narrow it down to just 5. Less is more!")
    else:
        try:
            # Send request to the API
            response = requests.post(API_URL, json=user_genres)
            if response.status_code == 200:
                prediction = response.json()["pred"]
                cluster_description = cluster_descriptions.get(prediction, "Unknown Cluster")
                st.success(f"🎉 Your movie type is: **{cluster_description}**")
                st.write("Here are some top recommendations just for you:")

                # Filter the DataFrame for recommendations
                recommended = df[df['Cluster'] == prediction]
                if not recommended.empty:
                    st.dataframe(recommended[['Title', 'Rating', 'Number of User Reviews', 'Genres']])
                else:
                    st.write("🤔 Hmm, no movies found for this cluster. Try another combination!")
            else:
                st.error("⚠️ Uh-oh! Something went wrong with the prediction. Try again later!")
        except Exception as e:
            st.error(f"💥 Yikes! An unexpected error occurred: {str(e)}")
