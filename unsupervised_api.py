from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib

# Load the model and scaler
model = joblib.load('kmeans_model.joblib')
scaler = joblib.load('scaler.joblib')

app = FastAPI()

# Define a Pydantic model for input validation
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
    # Convert input features to a dictionary
    dict_f = input_features.dict()

    # Ensure the dictionary keys match the expected order
    sorted_keys = [
        'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
        'Documentary', 'Drama', 'Family', 'Fantasy', 'Film_Noir', 'History',
        'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Romance', 'Sci_Fi',
        'Sport', 'Thriller', 'Unknown', 'War', 'Western'
    ]
    features_list = [dict_f[key] for key in sorted_keys]

    # Ensure the input is 2D for the scaler
    scaled_features = scaler.transform([features_list])  # Reshape to 2D
    return scaled_features


@app.post("/predict")
async def predict(input_features: InputFeatures):
    try:
        # Preprocess the input
        data = preprocessing(input_features)
        genre_vector = np.array(data).reshape(1, -1)
        
        # Predict the cluster
        y_pred = model.predict(genre_vector)
        return {"pred": int(y_pred[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
