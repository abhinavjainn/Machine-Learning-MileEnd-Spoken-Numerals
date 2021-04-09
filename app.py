import pickle
import numpy as np
from flask import Flask, request

def load_model():
    global model
    with open('model_19900_70_C10_G0_train975.pkl', 'rb') as f:
        model = pickle.load(f)

model = None
app = Flask(__name__)
load_model()

@app.route('/')
def home_endpoint():
    return 'Mile End Spoken Numerals, Get a prediction via /predict-intonation endpoint.', 200

@app.route('/predict-intonation', methods=['GET'])
def get_prediction():

    data = request.get_json()  
    data = np.array(data)[np.newaxis, :]
    try:
        prediction = model.predict(data)  
    except:
        return ("Model could not be loaded"), 404
    
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

if __name__ == '__main__':
    load_model() 
    app.run(host='0.0.0.0')
