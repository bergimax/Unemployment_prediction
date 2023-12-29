# # LOAD A MODEL
import pickle
from flask import Flask
from flask import request
from flask import jsonify

model_file = 'unemployment.bin'

with open(model_file, 'rb') as f_in: 
    dv, model = pickle.load(f_in) 

app = Flask('unemploy')

@app.route('/predict', methods=['POST'])

#create data to test it

def predict():
  unemploy = request.get_json()

  X = dv.transform(unemploy)
  y_pred = model.predict(X)

  result = {
     "unemploy": float(y_pred)
  }

  return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)