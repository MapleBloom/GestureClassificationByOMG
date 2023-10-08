from flask import Flask, request, jsonify
import json
import numpy as np

import pickle


# Read the model pipeline
with open('model/gesture_model.pkl', 'rb') as f:
    gesture_model = pickle.load(f)
    print(f'\nModel is ready.\n')


SENS = 40  # number of sensors
SMINI = 5  # time ticks at one minisample - parameter of our model - "time window"
   
    
def window_smini_x(Xdf: np.ndarray) -> np.ndarray:
    """Make X as SMINI-time ticks window, reshape to plain 2D-array.

    Args:
        Xdf (np.ndarray): source of X-data

    Returns:
        np.ndarray: X
    """    
    X = np.expand_dims(Xdf[SMINI-1:], axis=2)
    for i in range(2, SMINI + 1):
        X = np.concatenate((X, np.expand_dims(Xdf[SMINI-i:-i+1], axis=2)), axis=2)
    X = X.reshape((X.shape[0], SMINI * SENS))
    X = np.concatenate((np.repeat(X[0:1], 4, axis=0), X), axis=0)
    return X


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    server_name = request.args.get('server')
    return f'Test message. The server {server_name} is running'


@app.route('/predict', methods=['POST'])
def predict():
    r = json.loads(request.json)
    try:
        features = np.array(r).reshape(len(r) // SENS, SENS)
        X_test = window_smini_x(features)
        print('X_test shape', X_test.shape)
        pred = gesture_model.predict(X_test)
        print('prediction shape', pred.shape)
    except:
        return 'bad request', 400
    return jsonify({
        'prediction': pred.tolist()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
