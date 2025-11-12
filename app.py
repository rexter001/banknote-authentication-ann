from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load pre-trained scaler and model
MODEL_PATH = 'model.pkl'
SCALER_PATH = 'scaler.pkl'

# Load model and scaler
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("⚠️ Model files not found. Make sure model.pkl and scaler.pkl are in the app directory.")
    model = None
    scaler = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract features from request
        features = [
            float(data.get('variance')),
            float(data.get('skewness')),
            float(data.get('curtosis')),
            float(data.get('entropy'))
        ]
        
        # Scale features
        features_scaled = scaler.transform([features])
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probability = float(prediction)
        
        # Determine class
        if probability >= 0.5:
            result = "🔴 Forged Banknote"
            confidence = (probability * 100)
        else:
            result = "✅ Genuine Banknote"
            confidence = ((1 - probability) * 100)
        
        return jsonify({
            'success': True,
            'result': result,
            'confidence': round(confidence, 2),
            'probability': round(probability, 4)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/info', methods=['GET'])
def info():
    return jsonify({
        'name': 'Banknote Authentication System',
        'version': '1.0',
        'features': ['Variance', 'Skewness', 'Curtosis', 'Entropy'],
        'model': 'Artificial Neural Network (ANN)'
    })

if __name__ == '__main__':
    app.run(debug=True)
