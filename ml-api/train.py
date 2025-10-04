import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

MODEL_FILE = 'credit_model.pkl'
SCALER_FILE = 'scaler.pkl'
DATA_FILE = 'credit_data.csv'

def train_and_save_model():
    print(f"Loading data from {DATA_FILE}...")
    try:
        # CRITICAL FIX: Use sep='\s+' to handle space-separated data with no header
        data = pd.read_csv(DATA_FILE, sep='\s+', header=None)
    except FileNotFoundError:
        print(f"ERROR: {DATA_FILE} not found. Please ensure the correct file is in the ml-api folder.")
        return

    # Assign meaningful column names based on the UCI standard structure
    data.columns = ['checking_status', 'duration', 'credit_history', 'purpose', 'credit_amount', 'savings_status', 'employment', 'installment_rate', 'personal_status', 'other_parties', 'residence_since', 'property_magnitude', 'age', 'other_payment_plans', 'housing', 'existing_credits', 'job', 'num_dependents', 'own_telephone', 'foreign_worker', 'risk']

    # CRITICAL: Convert the target variable (risk) to 0 (good) and 1 (bad).
    # In the UCI dataset, 1 = Good and 2 = Bad.
    data['risk'] = data['risk'].apply(lambda x: 0 if x == 1 else 1)

    # Features selected to proxy for our simple frontend inputs (Age, Credit Capacity, Stability)
    features = data[['age', 'credit_amount', 'duration']]
    target = data['risk']

    # Data cleaning and splitting
    features = features.fillna(features.mean())

    # Scaling Features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Split data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(scaled_features, target, test_size=0.2, random_state=42)

    # Train the Model
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_test, y_test)
    print(f"Model trained. Accuracy on test set: {accuracy:.2f}")

    # Save the Model and Scaler
    joblib.dump(model, MODEL_FILE)
    joblib.dump(scaler, SCALER_FILE)
    print(f"\nModel and scaler saved as {MODEL_FILE} and {SCALER_FILE}.")

if __name__ == '__main__':
    train_and_save_model()