import pickle
import numpy as np
from flask import Flask, request

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
load_model()

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
    model_input = np.array(data)[np.newaxis, :]
    
    try:
        # Call the model instance to make predictions for intonation
        prediction = model.predict(model_input)  
    except:
        # Error if model instance not found
        return ("Model could not be loaded"), 404
    
    # Return prediction by mapping predicted numeric label to corresponding intonation
    if prediction[0]==1:  
        return ("Prediction for intonation is: "+"Question"), 200
    elif prediction[0]==2:
        return ("Prediction for intonation is: "+"Excited"), 200
    elif prediction[0]==3:
        return ("Prediction for intonation is: "+"Neutral"), 200
    elif prediction[0]==4:                        
        return ("Prediction for intonation is: "+"Bored"), 200
    else:    
        return ("Prediction for intonation is: "+"Unknown, or there may be an error"), 404

# Required for local testing
if __name__ == '__main__':
    app.run(host='0.0.0.0')
