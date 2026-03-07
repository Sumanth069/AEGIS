from agents.behavior_agent import analyze_behavior
from agents.network_agent import network_risk
from models.credit_model import predict_credit_risk
from models.fraud_model import train_fraud_model, fraud_probability
from agents.explanation_agent import generate_explanation


def generate_report(df):

    fraud_model = train_fraud_model(df)

    behavior = analyze_behavior(df)
    fraud = fraud_probability(fraud_model, df)
    credit = predict_credit_risk(df)
    network = network_risk(df)

    final_risk = (
        0.35 * fraud +
        0.25 * behavior +
        0.25 * credit +
        0.15 * network
    )

    report = f"""
Behaviour Risk: {behavior}
Fraud Risk: {fraud}
Credit Risk: {credit}
Network Risk: {network}
Final Risk: {final_risk}
"""

    explanation = generate_explanation(report)

    return behavior, fraud, credit, network, final_risk, explanation