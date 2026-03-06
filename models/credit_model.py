import random

def predict_credit_risk():

    default_probability = random.uniform(0.1,0.7)

    credit_risk = default_probability * 100

    return round(credit_risk,2), round(default_probability,2)