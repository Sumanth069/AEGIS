import pandas as pd

def network_risk_score():

    try:
        flagged = pd.read_csv("data/flagged_accounts.csv")

        flagged_count = len(flagged)

        if flagged_count > 50:
            return 60
        elif flagged_count > 20:
            return 40
        else:
            return 20

    except:
        return 10