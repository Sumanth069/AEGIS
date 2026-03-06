import streamlit as st
from engine.risk_engine import generate_report

st.set_page_config(page_title="AEGIS Risk Monitor", layout="wide")

st.title("🛡️ AEGIS – AI Financial Threat Intelligence")

st.write("Automated financial fraud and risk detection system")

# Example input values
fraud = st.slider("Fraud Probability (%)", 0, 100, 18)
credit = st.slider("Credit Risk (%)", 0, 100, 42)
financial = st.slider("Financial Weakness (%)", 0, 100, 30)
sentiment = st.slider("Negative News Sentiment (%)", 0, 100, 60)

if st.button("Generate Risk Report"):

    score, level, recommendation = generate_report(
        fraud/100,
        credit/100,
        financial/100,
        sentiment/100
    )

    st.subheader("📊 AEGIS Risk Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Fraud Probability", f"{fraud}%")
        st.metric("Credit Risk", f"{credit}%")

    with col2:
        st.metric("Financial Weakness", f"{financial}%")
        st.metric("Negative Sentiment", f"{sentiment}%")

    st.divider()

    st.subheader("🚨 Final Risk Assessment")

    st.metric("Final Risk Score", f"{score:.2f}/100")

    if level == "HIGH RISK":
        st.error(level)
    elif level == "MEDIUM RISK":
        st.warning(level)
    else:
        st.success(level)

    st.write("### Recommendation")
    st.write(recommendation)