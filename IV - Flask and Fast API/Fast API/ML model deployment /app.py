# 1. Importing all the necessary libraries

import uvicorn # importing this library since fastAPI uses ASGI (Asynchronous Server Gateway Interface)
from fastapi import FastAPI 
import pickle # since we need to use the classifier file back again
import numpy as np
import pandas as pd
from BankNote import BankNote # importing the data class to map values

# 2. Creating the app and unpicking the ML library
app = FastAPI()

# opening pickle library in rb mode
pickle_in = open("classifier.pkl", "rb")
classifier = pickle.load(pickle_in) # loading the pickle file which into the classifier

# 3. Creating the required APIs

# Index page route
@app.get('/')
def index():
    return {'message': 'Hello, World!'}

# Creating a simple API with GET request to display the name entered through the URL
@app.get('/{name}')
def greet_user(name: str):
    return {'Hi Welcome to this world, ': f'{name}'}


# Creating a API with POST request which accepts the parameters mentioned in the BankNote class
@app.post("/predict")
def predict_banknote(data: BankNote):

    # once the data is passed in form of banknote class, we are going ahead and converting it into a Dictionary
    # for better accessibility
    dict = data.model_dump()

    # extracting the parameters and storing in the corresponding variables
    variance = dict["variance"]
    skewness = dict["skewness"]
    curtosis = dict["curtosis"]
    entropy = dict["entropy"]

    # passing the above variables into the model which we have loaded
    prediction = classifier.predict([[variance, skewness, curtosis, entropy]])

    response = ""

    # wring a simple if condition based on the output of the prediction
    if prediction[0] > 0.5:
        response = "Its a genuine note"
    else:
        response = "Its a Forged/Fake note"

    return {'response' : response}


# Running the FastAPI app on port 8000 and on localhost using uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)