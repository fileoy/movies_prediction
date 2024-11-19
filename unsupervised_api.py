from fastapi import FastAPI, HTTPException
import numpy as np
import joblib
model = joblib.load('kmeans_model.joblib')
scaler = joblib.load('scaler.joblib')
app = FastAPI()


# GET request
@app.get("/")
def read_root():
    return {"message": "Welcome to Tuwaiq Academy"}
# get request
@app.get("/items/")
def create_item(item: dict):
    return {"item": item}

from pydantic import BaseModel
# Define a Pydantic model for input data validation
class InputFeatures(BaseModel):
    Action: int  
    Adventure: int  
    Animation: int  
    Biography: int  
    Comedy: int  
    Crime: int  
    Documentary: int  
    Drama: int  
    Family: int  
    Fantasy: int  
    Film_Noir: int  
    History: int  
    Horror: int  
    Music: int  
    Musical: int  
    Mystery: int  
    News: int  
    Romance: int  
    Sci_Fi: int  
    Sport: int  
    Thriller: int  
    Unknown: int  
    War: int  
    Western: int  



def preprocessing(input_features: InputFeatures):

    dict_f = {
        'Action': input_features.Action,
        'Adventure': input_features.Adventure,
        'Animation': input_features.Animation,
        'Biography': input_features.Biography,
        'Comedy': input_features.Comedy,
        'Crime': input_features.Crime,
        'Documentary': input_features.Documentary,
        'Drama': input_features.Drama,
        'Family': input_features.Family,
        'Fantasy': input_features.Fantasy,
        'Film-Noir': input_features.Film_Noir,
        'History': input_features.History,
        'Horror': input_features.Horror,
        'Music': input_features.Music,
        'Musical': input_features.Musical,
        'Mystery': input_features.Mystery,
        'News': input_features.News,
        'Romance': input_features.Romance,
        'Sci-Fi': input_features.Sci_Fi,
        'Sport': input_features.Sport,
        'Thriller': input_features.Thriller,
        'Unknown': 0,
        'War': input_features.War,
        'Western': input_features.Western,
    }

    # Convert dictionary values to a list in the correct order
    features_list = [dict_f[key] for key in sorted(dict_f)]
    # Scale the input features
    scaled_features = scaler.transform(features_list)
    return scaled_features


@app.get("/predict")
def predict(input_features: InputFeatures):
    return preprocessing(input_features)

@app.post("/predict")
async def predict(input_features: InputFeatures):
    data = preprocessing(input_features)
    genre_vector = np.array(data).reshape(1, -1)
    y_pred = model.predict(genre_vector)
    return {"pred": y_pred.tolist()[0]}
