import pandas as pd

def analyze_transactions(file):

    df = pd.read_csv(file)

    # Fraud ratio in dataset
    fraud_transactions = df[df["Class"] == 1]

    fraud_ratio = len(fraud_transactions) / len(df)

    behaviour_risk = fraud_ratio * 100

    return round(behaviour_risk, 2)