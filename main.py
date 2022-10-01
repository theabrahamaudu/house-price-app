import joblib
from fastapi import FastAPI
import uvicorn
import pandas as pd
import numpy as np
from pydantic import BaseModel


# Initialize FastAPI
app = FastAPI(title='House Price App',
              version='1.0',
              description='Linear Regression model is used for prediction'
              )
# Import Model
model = joblib.load('LinearRegressionModel.joblib')


# Data Validation
class Data(BaseModel):
    bedrooms: float
    bathrooms: float
    toilets: float
    parking_space: float
    house_type: str
    town: str
    state: str


# API home endpoint
@app.get('/')
@app.get('/home')
def read_home():
    """
    Home endpoint which can be used to test the availability of the    application.
    """
    return {'message': 'System is healthy'}


# Prediction endpoint
@app.post("/predict")
def predict(data: Data):
    result = model.predict(pd.DataFrame(columns=['bedrooms',
                                                 'bathrooms',
                                                 'toilets',
                                                 'parking_space',
                                                 'house_type',
                                                 'town',
                                                 'state'],
                                        data=np.array([data.bedrooms,
                                                       data.bathrooms,
                                                       data.toilets,
                                                       data.parking_space,
                                                       data.house_type,
                                                       data.town,
                                                       data.state]).reshape(1, 7)))[0]
    return result


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)