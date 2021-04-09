import pickle
import numpy as np
from flask import Flask, request

model = None
app = Flask(__name__)

def load_model():
    global model
    with open('model_19900_70_C10_G0_train975.pkl', 'rb') as f:
        model = pickle.load(f)

@app.route('/')
def home_endpoint():
    return 'Mile End Spoken Numerals, Get a prediction via /predict-intonation endpoint.'

@app.route('/predict-intonation', methods=['GET'])
def get_prediction():

    data = request.get_json()  
    data = np.array(data)[np.newaxis, :]
    prediction = model.predict(data)  
    
    if prediction[0]==1:
        return ("Prediction for intonation is: "+"Question")
    elif prediction[0]==2:
        return ("Prediction for intonation is: "+"Excited")
    elif prediction[0]==3:
        return ("Prediction for intonation is: "+"Neutral")
    elif prediction[0]==4:                        
        return ("Prediction for intonation is: "+"Bored")
    else:    
        return ("Prediction for intonation is: "+"Unknown, or there may be an error")

if __name__ == '__main__':
    load_model() 
    app.run(host='0.0.0.0')
