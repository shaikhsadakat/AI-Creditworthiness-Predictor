import json
import random
from flask import Flask, request, jsonify
from flask_cors import CORS # This allows the frontend to talk to this server

# --- Mock Model Placeholder ---
# When you train your real model, the loading code goes here.
# -----------------------------

app = Flask(__name__)
# Allow cross-origin requests from any source for development ease.
CORS(app) 

def mock_predict_score(data):
    """
    MOCK function to calculate a credit score based on alternative data inputs.
    """
    try:
        # 1. Extract and convert inputs to numbers
        income = float(data.get('monthly_income', 0))
        rent = float(data.get('monthly_rent', 0))
        utilities = float(data.get('on_time_utilities', 0))
        employment = float(data.get('employment_years', 0))

        # 2. Simple Scoring Logic (Simulates ML output)
        base_score = 400.0
        income_factor = (income / 5000) * 100
        income_ratio = 1 - (rent / income) if income > rent and income > 0 else 0
        rent_factor = income_ratio * 75
        utilities_factor = utilities * 12
        employment_factor = min(employment, 8) * 15

        predicted_score = round(base_score + income_factor + rent_factor + utilities_factor + employment_factor + random.uniform(-25, 25))
        
        # Clamp score to 300-850 range
        predicted_score = max(300, min(850, predicted_score))

        # 3. Determine Risk and Default Probability
        default_probability = round(max(0.02, (900 - predicted_score) / 600), 2)
        risk_level = 'Low' if predicted_score >= 700 else ('Moderate' if predicted_score >= 600 else 'High')
        
        return {
            'credit_score': predicted_score,
            'default_probability': default_probability,
            'risk_level': risk_level
        }

    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/ml/predict', methods=['POST'])
def predict_creditworthiness():
    """Endpoint for prediction requests."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No input data provided.'}), 400
            
        prediction_result = mock_predict_score(data)
        
        if 'error' in prediction_result:
             return jsonify(prediction_result), 500

        return jsonify(prediction_result)

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def status_check():
    """Simple health check endpoint."""
    return "AI Creditworthiness Predictor ML API is running.", 200

if __name__ == '__main__':
    # Runs the server on port 5000
    app.run(debug=True, port=5000)