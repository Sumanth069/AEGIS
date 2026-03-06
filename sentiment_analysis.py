import pandas as pd
from transformers import pipeline

print("\n========== AEGIS NEWS SENTIMENT ANALYSIS ==========\n")

# Load news dataset
data = pd.read_csv("data/news_data.csv")

# Load sentiment model
sentiment_model = pipeline("sentiment-analysis")

for index, row in data.iterrows():

    company = row["company"]
    headline = row["headline"]

    result = sentiment_model(headline)[0]

    sentiment = result["label"]
    confidence = result["score"]

    print(f"Company: {company}")
    print(f"News: {headline}\n")

    print(f"Sentiment: {sentiment}")
    print(f"Confidence: {round(confidence,2)}")

    if sentiment == "NEGATIVE":
        print("⚠ Reputation Risk Detected")

    print("\n--------------------------------------\n")