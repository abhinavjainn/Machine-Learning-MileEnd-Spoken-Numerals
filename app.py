import pickle
import numpy as np
from flask import Flask, request
from flask_restful import Api
import os
from db import db
import uuid
from models.logs import LogsModel
from datetime import datetime, date
import time

def load_model():
    '''
    Load the model from disk.
    Retruns: Model instance    
    '''
    global model
    with open('model_19900_70_C10_G0_train975.pkl', 'rb') as f:
        model = pickle.load(f)

model = None
app = Flask(__name__)
db.init_app(app)
load_model()

@app.before_first_request
def create_tables():
    db.create_all()

# App configuration: Database and app secret key
db_url = os.environ.get('DATABASE_URL')                                   # For Heroku, comment for local execution 
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("://", "ql://", 1) # For Heroku, comment for local execution
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'             # For Local, comment for Heroku execution  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'MileEndNumerals'
api = Api(app)

# Endpoint: Home
@app.route('/')
def home_endpoint():
    return 'You are at home page of "Mile End Spoken Numerals". Get a prediction via /predict-intonation endpoint.', 200

# Endpoint: predict-intonation
@app.route('/predict-intonation', methods=['GET'])
def get_prediction():
    '''
    Makes prediction for intonation using the input from json request.
    Returns: Predicted intonation
    '''

    # Get JSON request data
    data = request.get_json() 
    # Convert 1-d list input to 2-d numpy aaray 
    model_input_raw = np.array(data)
    model_input = model_input_raw[np.newaxis, :]
    
    try:
        # Call the model instance to make predictions for intonation
        prediction = model.predict(model_input)  
    except:
        # Error if model instance not found
        return ("Model could not be loaded"), 404

    # Return prediction by mapping predicted numeric label to corresponding intonation
    if prediction[0]==1:  
        model_log(model_input_raw,prediction[0],"Question")
        return ("Prediction for intonation is: "+"Question"), 200
    elif prediction[0]==2:
        model_log(model_input_raw,prediction[0],"Excited")
        return ("Prediction for intonation is: "+"Excited"), 200
    elif prediction[0]==3:
        model_log(model_input_raw,prediction[0],"Neutral")
        return ("Prediction for intonation is: "+"Neutral"), 200
    elif prediction[0]==4:            
        model_log(model_input_raw,prediction[0],"Bored")            
        return ("Prediction for intonation is: "+"Bored"), 200
    else:   
        return ("Prediction for intonation is: "+"Unknown, or there may be an error"), 404

def model_log(model_in,pred_num,pred_str):
    '''
    Log model usage data in the database for monitoring model performance

    Input: model input, model prediction
    Action: Save model input, prediction along with date time and timezone
    '''

    uid = str(uuid.uuid4())
    datenow = date.today().strftime("%d.%m.%Y")
    timenow = datetime.now().strftime("%H:%M:%S")
    tznow = time.tzname[0]

    logs = LogsModel(uid, str(model_in), pred_num, pred_str, datenow, timenow, tznow)
    logs.save_to_db()

# Required for local testing
if __name__ == '__main__':
    app.run(host='0.0.0.0')
