from agents.financial_agent import analyze_transactions
from agents.network_agent import network_risk_score
from models.credit_model import predict_credit_risk
from agents.explanation_agent import generate_explanation


def generate_report(name, loan_amount, transaction_file):

    behaviour_risk = analyze_transactions(transaction_file)

    network_risk = network_risk_score()

    credit_risk, default_probability = predict_credit_risk()

    final_risk = behaviour_risk + network_risk + credit_risk

    if final_risk < 40:
        recommendation = "APPROVE LOAN"

    elif final_risk < 80:
        recommendation = "MANUAL INVESTIGATION"

    else:
        recommendation = "REJECT"

    report = {
        "name": name,
        "behaviour_risk": behaviour_risk,
        "credit_risk": credit_risk,
        "network_risk": network_risk,
        "default_probability": default_probability,
        "final_risk": round(final_risk,2),
        "recommendation": recommendation
    }

    explanation = generate_explanation(report)

    report["explanation"] = explanation

    return report