# -----------------------------
# Imports
# -----------------------------

# FastAPI is used to create the API
from fastapi import FastAPI

# Pydantic is used for data validation and schema definition
from pydantic import BaseModel

# Pandas is used to convert input data into a DataFrame
import pandas as pd

# Joblib is used to load the trained machine learning artifact
import joblib


# -----------------------------
# Initialize FastAPI application
# -----------------------------

app = FastAPI(
    title="Customer Churn Prediction API - V2",
    description="API that predicts customer churn probability using an XGBoost model with an optimized threshold",
    version="2.0"
)


# -----------------------------
# Load trained model artifact
# -----------------------------

# This file contains:
# - model: full preprocessing + XGBoost pipeline
# - threshold: optimized decision threshold selected during model evaluation
artifact = joblib.load("churn_model_v2.joblib")

model = artifact["model"]
threshold = artifact["threshold"]


# -----------------------------
# Define input data schema
# -----------------------------

# This class validates incoming requests automatically:
# - ensures correct data types
# - ensures required fields are present
# - helps generate API documentation (Swagger)
class CustomerData(BaseModel):
    customerID: str
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


# -----------------------------
# Health check endpoint
# -----------------------------

# This endpoint is used to verify that the API is running correctly
@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API V2 is running",
        "model_version": "v2",
        "threshold": threshold
    }


# -----------------------------
# Model information endpoint
# -----------------------------

# This endpoint helps reviewers understand the deployed model configuration
@app.get("/model-info")
def model_info():
    return {
        "model": "XGBoost",
        "model_version": "v2",
        "threshold": threshold,
        "objective": "Predict customer churn probability"
    }


# -----------------------------
# Main prediction endpoint
# -----------------------------

@app.post("/predict")
def predict(customer: CustomerData):

    # Convert incoming JSON data into a DataFrame
    # The model expects the same structure used during training
    data = pd.DataFrame([customer.model_dump()])

    # Generate probability of churn
    churn_probability = model.predict_proba(data)[0][1]

    # Apply optimized threshold from Version 2
    prediction = int(churn_probability >= threshold)

    # Add a simple business-friendly label
    prediction_label = "Churn" if prediction == 1 else "No Churn"

    # Return results as JSON response
    return {
        "prediction": prediction,
        "prediction_label": prediction_label,
        "churn_probability": float(churn_probability),
        "threshold_used": float(threshold)
    }
