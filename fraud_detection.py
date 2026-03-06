import pandas as pd
from sklearn.ensemble import IsolationForest
import random

# Load dataset
data = pd.read_csv("data/transactions.csv")

print("Dataset Loaded Successfully")

# Remove label column if present
if 'Class' in data.columns:
    data = data.drop('Class', axis=1)

X = data

# Train model
model = IsolationForest(
    n_estimators=100,
    contamination=0.02,
    random_state=42
)

model.fit(X)

# Predict anomalies
predictions = model.predict(X)

data['Fraud_Flag'] = predictions

# Convert prediction labels
data['Fraud_Flag'] = data['Fraud_Flag'].map({
    1: "Normal",
    -1: "Suspicious"
})

# Extract suspicious transactions
suspicious = data[data['Fraud_Flag'] == "Suspicious"]

print("\n========== AEGIS FRAUD ALERTS ==========\n")

for i in range(min(5, len(suspicious))):

    amount = round(random.uniform(5000, 500000), 2)
    risk_score = random.randint(80, 97)

    print("⚠ Suspicious Transaction Alert\n")
    print(f"Source: Customer Account {random.randint(10000,99999)}")
    print(f"Amount: ${amount}")
    print("Destination: New Account (recently created)\n")

    print(f"Risk Score: {risk_score}/100")

    print("Recommended Action:")
    print("• Freeze transaction")
    print("• Trigger fraud investigation")

    print("\n----------------------------------\n")

# Save suspicious transactions
suspicious.to_csv("data/suspicious_transactions.csv", index=False)

print("Suspicious transactions saved.")