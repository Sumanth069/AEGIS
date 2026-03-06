def generate_explanation(report):

    behaviour = report["behaviour_risk"]
    credit = report["credit_risk"]
    network = report["network_risk"]
    final = report["final_risk"]

    explanation = "AI Investigation Summary:\n\n"

    if behaviour > 40:
        explanation += "- The transaction history shows unusual behavioural patterns.\n"
    else:
        explanation += "- The transaction behaviour appears mostly stable.\n"

    if credit > 50:
        explanation += "- The credit model predicts a higher probability of default.\n"
    else:
        explanation += "- The applicant shows moderate credit risk.\n"

    if network > 40:
        explanation += "- The account shows connections with flagged or suspicious entities.\n"
    else:
        explanation += "- No strong suspicious network connections were detected.\n"

    explanation += "\nOverall Risk Score: " + str(final)

    if final < 40:
        explanation += "\nAI Recommendation: The loan application appears safe to approve."

    elif final < 80:
        explanation += "\nAI Recommendation: Further manual investigation is advised before approval."

    else:
        explanation += "\nAI Recommendation: High financial risk detected. Loan rejection is recommended."

    return explanation