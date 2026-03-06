from engine.risk_engine import generate_report

report = generate_report(
    name="Rahul",
    loan_amount=200000,
    transaction_file="transactions.csv"
)

print("\nAEGIS RISK REPORT\n")

print("Customer:", report["name"])
print("Behaviour Risk:", report["behaviour_risk"])
print("Credit Risk:", report["credit_risk"])
print("Network Risk:", report["network_risk"])
print("Default Probability:", report["default_probability"])

print("\nFinal Risk Score:", report["final_risk"])
print("Recommendation:", report["recommendation"])