# AI Creditworthiness Predictor (For the Unbanked)

## 🌟 Project Overview

This project is a Proof-of-Concept (PoC) for a disruptive Fintech solution designed to address **financial exclusion**. It uses Machine Learning (ML) to predict the creditworthiness and default risk of individuals who lack a traditional credit history (the "unbanked" or "credit-invisible").

Instead of relying on traditional credit scores, the application analyzes **alternative data proxies** (simulated income, stable housing payments, employment history) to determine loan eligibility.

### The Problem

Globally, billions of people lack access to basic financial services because traditional lending models require a lengthy credit history. This leaves otherwise creditworthy individuals unable to secure capital.

### The Solution

We built a hybrid application that uses alternative financial and behavioral data points to calculate a predicted credit score and risk level in real-time. The score is based on a trained ML model, and the application is deployed entirely on **free, non-commercial hosting tiers**.

## ⚡ Live Demo

Experience the app in action and see how alternative data can be used to predict a credit score in real-time.

**Live on Netlify:** https://ai-creditworthiness-predictor.netlify.app/

## 🛠️ Technology Stack (Hybrid MERN + Python Microservices)

This project uses a modern, three-tier microservice architecture to separate the business logic, the core ML computation, and the user interface.

| Component | Technology | Role | Free Hosting Platform |
| :--- | :--- | :--- | :--- |
| **Frontend** (UI) | HTML, Vanilla JavaScript, Tailwind CSS, Chart.js | Handles user input, calls the Express API, and displays results and history. | Netlify (Static Hosting) |
| **Backend Proxy** (API) | Node.js, Express.js, Axios, Firebase Admin SDK | Proxies frontend requests to the Python ML API and securely saves prediction history to the database. | Render (Web Service) |
| **ML API** (Core Logic) | Python, Flask, Scikit-learn, Gunicorn, Pipelines | Loads the trained, enhanced credit prediction model (`credit_model_v2.pkl`) and calculates the real-time risk score. | Render (Web Service) |
| **Database** | Firebase Firestore | Cloud NoSQL database used to persist and retrieve user prediction history. | Google Firebase (Free Tier) |
| **Data Source** | UCI German Credit Data | Used to train the predictive model, mapping complex features to simple input proxies. | Kaggle/UCI |

## 🚀 Deployment and Usage

### Local Setup (Development)

To run the full application locally, you must run three separate commands in three terminals:

1.  **Python ML API (Port 5000) - The Brain**
    ```bash
    # From the ml-api directory, with venv activated
    py app.py
    ```

2.  **Express Backend Proxy (Port 3001) - The Traffic Cop**
    ```bash
    # From the backend directory
    node server.js
    ```

3.  **Frontend (Browser)**
    Open the `index.html` file in your browser (Live Server recommended).

### Cloud Deployment (Free Tiers)

The entire application is deployed using free services. The `index.html` file calls the public URL of the Render Express Proxy.

| Service | Hosting | GitHub Folder | Key Secrets (Set on Host) |
| :--- | :--- | :--- | :--- |
| **Frontend** | Netlify | `/` (root) | None |
| **ML API** | Render | `/ml-api` | None |
| **Express Proxy** | Render | `/backend` | `FIREBASE_SERVICE_ACCOUNT`, `PYTHON_ML_API_URL` |

## 🧠 Machine Learning Details (V2 Enhanced Model)

The predictive core uses an enhanced model pipeline to achieve better accuracy by incorporating multiple feature types.

* **Model:** Logistic Regression (Binary Classification).
* **Target Variable:** Credit Risk (0 = Good Credit, 1 = Bad Credit).
* **Feature Engineering:** The model uses a **Scikit-learn Pipeline** to correctly handle data:
    * **Numerical Features:** `age`, `credit_amount`, `duration` (Scaled using `StandardScaler`).
    * **Categorical Features:** `checking_status`, `credit_history`, `employment`, `purpose` (Encoded using `OneHotEncoder`).
* **Scoring Logic:** The model's predicted probability of default ($P_{default}$) is converted into a score (300-850 range) using the formula: $Score = 850 - (550 \times P_{default})$.

## 🧑‍💻 Next Development Steps

Future enhancements could focus on production readiness and adding functionality:

1.  **Full User Authentication:** Integrate Firebase Authentication (Google/Email) to give each user their own private prediction history, replacing the static `anonymous_user_1` placeholder.
2.  **Model Explainability (XAI):** Integrate a tool like SHAP to show the user *why* a particular input (e.g., Employment Duration vs. Income) influenced their final score the most.
