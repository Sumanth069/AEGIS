import pandas as pd

# Load financial dataset
data = pd.read_csv("data/company_financials.csv")

print("\n========== AEGIS FINANCIAL ANALYSIS ==========\n")

for index, row in data.iterrows():

    company = row['company']
    revenue = row['revenue']
    profit = row['profit']
    debt = row['debt']
    equity = row['equity']
    assets = row['assets']
    liabilities = row['liabilities']
    cash_flow = row['cash_flow']

    # Calculate financial ratios
    debt_to_equity = debt / equity
    profit_margin = profit / revenue
    liquidity_ratio = assets / liabilities

    print(f"Company: {company}\n")

    print(f"Debt-to-Equity Ratio: {round(debt_to_equity,2)}")
    print(f"Profit Margin: {round(profit_margin*100,2)}%")
    print(f"Liquidity Ratio: {round(liquidity_ratio,2)}")
    print(f"Cash Flow: {cash_flow}")

    risk_flags = []

    if debt_to_equity > 2:
        risk_flags.append("High leverage")

    if profit_margin < 0.05:
        risk_flags.append("Low profitability")

    if liquidity_ratio < 1:
        risk_flags.append("Liquidity risk")

    if cash_flow < 0:
        risk_flags.append("Negative cash flow")

    if risk_flags:
        print("\n⚠ Financial Risk Signals Detected:")
        for flag in risk_flags:
            print(f"• {flag}")

    else:
        print("\nFinancial health appears stable.")

    print("\n--------------------------------------\n")