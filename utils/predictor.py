import pandas as pd
import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "loan_model.pkl")

model = joblib.load(MODEL_PATH)

def predict_loan_eligibility(income, credit, loan_amount, loan_term):
    df = pd.DataFrame({
        "Income": [income],
        "CreditScore": [credit],
        "LoanAmount": [loan_amount],
        "LoanTerm": [loan_term]
    })
    prediction = model.predict(df)
    return prediction[0] == 1
