import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load and prepare dataset
df = pd.read_csv("dataset/loan_data.csv")
X = df.drop("Eligibility", axis=1)
y = df["Eligibility"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "models/loan_model.pkl")
print("Model trained and saved.")
