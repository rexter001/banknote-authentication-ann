from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# In-memory trained model (using a simple RandomForest for demo)
# In production, you would load a pre-trained model from a file
model = None
scaler = None

def load_or_create_model():
    """Load model or create a demo model"""
    global model, scaler
    
    # For Vercel deployment, we use a pre-trained RandomForest model
    # This is a fallback - ideally you'd have model.pkl and scaler.pkl
    try:
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print("✅ Model loaded from files")
    except FileNotFoundError:
        print("⚠️ Model files not found. Using demo model...")
        # Create a simple trained model for demo
        from sklearn.datasets import make_classification
        X_demo, y_demo = make_classification(
            n_samples=100, n_features=4, n_classes=2, random_state=42
        )
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_demo)
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_scaled, y_demo)
        print("✅ Demo model created")

# Load model on startup
load_or_create_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Extract features from request
        features = [
            float(data.get('variance', 0)),
            float(data.get('skewness', 0)),
            float(data.get('curtosis', 0)),
            float(data.get('entropy', 0))
        ]
        
        # Validate input
        if not all(isinstance(f, (int, float)) for f in features):
            return jsonify({
                'success': False,
                'error': 'All features must be numeric'
            }), 400
        
        # Scale features
        features_scaled = scaler.transform([features])
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probability = float(model.predict_proba(features_scaled)[0][1])
        
        # Determine class
        if prediction == 1:
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
        'model': 'Random Forest Classifier'
    })

if __name__ == '__main__':
    app.run(debug=True)
