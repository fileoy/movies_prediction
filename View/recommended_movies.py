
import streamlit as st
import pandas as pd


st.title("Movie Recommendations")
st.text(body="What was the last movie you watched that you would like to see a similar one to?")



df = pd.read_csv("data_with_cluster.csv")
df.drop(columns="Unnamed: 0",inplace=True)

# def get_genres_by_title(title):
#     row = df[df['Title'] == title]
#     if not row.empty:
#         return row['Cluster'].values[0]  # This returns the genres column
#     else:
#         return None  # Return None if title not found

# # Input for movie title
# title_input = st.text_input("Enter a Movie Name:")

# if title_input:
#     cluster = get_genres_by_title(title_input)
    
#     if cluster:
#         st.success(f"Genres for '{title_input}': {cluster}")
#     else:
#         st.error(f"No genres found for '{title_input}'. Please check the title.")
        
# clu =  get_genres_by_title(title_input) 





# recommended = df[df['Cluster'] == clu]
  

# if st.checkbox("Show recomended movies"):
#     st.dataframe(recommended[['Title','Rating','Number of User Reviews','Genres','Cluster']])





def get_genres_by_title(title):
    row = df[df['Title'] == title]
    if not row.empty:
        return row['Genres'].values[0]  
    else:
        return None  # Return None if title not found


st.title("Movie Finder")


title_input = st.text_input("Search for a Movie Name:")

# Filter the DataFrame based on the search input
if title_input:
    filtered_movies = df[df['Title'].str.contains(title_input, case=False, na=False)]
else:
    filtered_movies = pd.DataFrame(columns=df.columns)  # Empty DataFrame if no input


if not filtered_movies.empty:
    st.write("Suggestions:")
    for index, movie in enumerate(filtered_movies['Title'].values):
        
        if st.button(movie, key=f"{movie}_{index}"):  
            selected_movie = movie
            cluster = get_genres_by_title(selected_movie)
            
            if cluster:
                st.success(f"Genres for '{selected_movie}': {cluster}")
                
                # Find recommended movies based on the cluster
                clu = df[df['Title'] == selected_movie]['Cluster'].values[0]
                recommended = df[df['Cluster'] == clu]
                st.dataframe(recommended[['Title', 'Rating', 'Number of User Reviews','Year','Genres']])
            else:
                st.error(f"No genres found for '{selected_movie}'. Please check the title.")


