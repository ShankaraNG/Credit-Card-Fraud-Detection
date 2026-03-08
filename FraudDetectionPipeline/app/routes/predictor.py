from fastapi import APIRouter, HTTPException, Depends, Request
from app.schemas import Transaction
import pandas as pd
from app.services.preprocessing import clean_data
from app.services.modelloader import loadmodel
from typing import List
from app.logger import get_logger


log = get_logger('Router')

router = APIRouter()

# Load model once at the module level or via a startup event
MODEL = loadmodel()

@router.get("/")
def root():
    log.info("accessing the root directory")
    return {"message": "Welcome to the Credit Card detection API"}

@router.post("/predict")
def predictor(transactions: List[Transaction], request: Request):
    try:
        log.info("Getting the loaded model")
        model = getattr(request.app.state, "model", None)
        
        if model is None:
            raise HTTPException("Model is not initialized or is still loading.")
        log.info("Model retieved from the cache successfully")
        data = [t.model_dump() for t in transactions]
        df = pd.DataFrame(data)
        log.info("Data request recieved successfully")
        log.info(f"requested data:  {str(df.head(2))}")
        log.info("Cleaning the data")
        df_cleaned = clean_data(df)
        
        if df_cleaned is None or df_cleaned.empty:
            raise HTTPException("Data cleaning failed: output is empty or null")
        log.info("Data has been cleaned")
        log.info("Predicting the from the data")
        preds = model.predict(df_cleaned)
        probs = model.predict_proba(df_cleaned)[:, 1]
        log.info("Completed predictions")
        log.info("adding to the result")
        results = [
            {
                "prediction": "Fraud" if int(p) == 1 else "Good",
                "fraud_probability": round(float(prob), 4)
            }
            for p, prob in zip(preds, probs)
        ]
        log.info(f"Predictions: {results[:2]}")
        log.info("Request completed successfully")
        return results
    except Exception as e:
        log.error(f"Prediction Error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="An internal error occurred during prediction logic."
        )