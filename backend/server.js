const express = require('express');
const cors = require('cors');
const axios = require('axios');
const admin = require('firebase-admin');

const app = express();
// Use the port provided by the hosting environment (Render) or default to 3001 locally
const PORT = process.env.PORT || 3001; 
// Use the Python API's live URL (from environment variable) or local URL for development
const PYTHON_ML_API_URL = process.env.PYTHON_ML_API_URL || 'http://127.0.0.1:5000/api/ml/predict'; 

// --- Firebase Initialization (CRITICAL FOR DEPLOYMENT) ---
// Checks for the Firebase credentials environment variable (used on Render)
if (process.env.FIREBASE_SERVICE_ACCOUNT) {
    const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT);
    admin.initializeApp({
        credential: admin.credential.cert(serviceAccount)
    });
    console.log("Firebase initialized using environment variable.");
} else {
    // Fallback to local file for development (requires serviceAccountKey.json)
    try {
        const serviceAccount = require('./serviceAccountKey.json');
        admin.initializeApp({
            credential: admin.credential.cert(serviceAccount)
        });
        console.log("Firebase initialized using local file.");
    } catch (e) {
        console.error("WARNING: Firebase not initialized! Missing serviceAccountKey.json. Prediction history will fail.");
    }
}
const db = admin.firestore();
// --- End Firebase Initialization ---

// Middleware
app.use(cors());
app.use(express.json());

// Placeholder for user identification (In a real app, this comes from an auth token)
const userId = 'anonymous_user_1';

// Status check route: Fixes the 'Cannot GET /' error
app.get('/', (req, res) => {
    res.status(200).send('AI Creditworthiness Predictor Express Proxy is running.');
});


// --- ROUTE 1: GET Prediction History ---
app.get('/api/history', async (req, res) => {
    try {
        // Fetch all predictions for the anonymous user, limited to 10
        // NOTE: We removed the .orderBy('timestamp', 'desc') temporarily to fix the Key Error.
        const snapshot = await db.collection('predictions')
            .where('userId', '==', userId)
            .limit(10) 
            .get();
        
        const history = [];
        snapshot.forEach(doc => {
            const data = doc.data();
            
            // Format the timestamp for a cleaner display on the frontend
            const date = data.timestamp 
                ? data.timestamp.toDate().toLocaleTimeString('en-US', { 
                    hour: '2-digit', 
                    minute: '2-digit', 
                    month: 'short', 
                    day: 'numeric' 
                }) 
                : 'N/A';
            
            history.push({
                id: doc.id,
                score: data.credit_score,
                risk: data.risk_level,
                date: date,
                inputs: data.inputs 
            });
        });

        res.json(history);
    } catch (error) {
        console.error('Error fetching history from Firestore:', error);
        // This is the error message the frontend receives
        res.status(500).json({ error: 'Failed to retrieve history. Check server logs.' }); 
    }
});


// --- ROUTE 2: POST Prediction Request (Proxy) ---
app.post('/api/predict', async (req, res) => {
    const inputData = req.body;
    
    try {
        // 1. Forward the data to the Python ML API (either local 5000 or Render URL)
        const mlResponse = await axios.post(PYTHON_ML_API_URL, inputData);
        const prediction = mlResponse.data;

        // 2. Save the prediction to Firestore
        const predictionRecord = {
            userId: userId,
            timestamp: admin.firestore.FieldValue.serverTimestamp(),
            inputs: inputData,
            ...prediction
        };

        await db.collection('predictions').add(predictionRecord);
        console.log('Prediction successfully saved to Firestore.');
        
        // 3. Send the ML API's response back to the frontend
        res.json(prediction);
        
    } catch (error) {
        // This catches errors from the ML API or Firebase save operations
        console.error('Error calling ML API or writing to Firestore:', error.message);
        res.status(500).json({ 
            error: 'Failed to get prediction from ML Service or save to database.',
            details: error.message
        });
    }
});


app.listen(PORT, () => {
    console.log(`Express Backend Proxy running on http://localhost:${PORT}`);
    console.log(`Python ML API target: ${PYTHON_ML_API_URL}`);
});