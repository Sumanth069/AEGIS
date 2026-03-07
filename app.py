import streamlit as st
import pandas as pd
import plotly.express as px

from engine.risk_engine import generate_report

# Page configuration
st.set_page_config(
    page_title="AEGIS Financial Threat Intelligence",
    layout="wide"
)

# Title
st.title("🛡 AEGIS Financial Threat Intelligence Engine")

st.write("Upload a transaction dataset to analyze fraud risk, behavioural anomalies, and credit intelligence.")

# Upload dataset
uploaded_file = st.file_uploader("Upload Transaction CSV")

if uploaded_file:

    # Load dataset
    df = pd.read_csv(uploaded_file)

    # SPEED FIX FOR LARGE DATASET
    if len(df) > 20000:
        df = df.sample(20000)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Run analysis button
    if st.button("Run AEGIS Analysis"):

        # Spinner so user sees progress
        with st.spinner("Running AEGIS Threat Intelligence Engine..."):

            behavior, fraud, credit, network, final, explanation = generate_report(df)

        st.success("Analysis Complete")

        st.divider()

        # =============================
        # Threat Intelligence Metrics
        # =============================

        st.subheader("Threat Intelligence Metrics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Behaviour Risk", round(behavior, 3))
        col2.metric("Fraud Probability", round(fraud, 3))
        col3.metric("Credit Risk", round(credit, 3))
        col4.metric("Network Risk", round(network, 3))

        st.divider()

        # =============================
        # Final Risk Score
        # =============================

        st.subheader("Final Risk Score")

        st.success(round(final, 3))

        st.divider()

        # =============================
        # Transaction Analytics
        # =============================

        st.subheader("Transaction Amount Distribution")

        fig = px.histogram(
            df,
            x="amount",
            nbins=50,
            title="Transaction Amount Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # =============================
        # Suspicious Transactions
        # =============================

        st.subheader("Potentially Suspicious Transactions")

        suspicious = df[df["amount"] > df["amount"].quantile(0.99)]

        st.dataframe(suspicious.head(20))

        st.divider()

        # =============================
        # AI Investigation Report
        # =============================

        st.subheader("AI Financial Investigation Report")

        st.write(explanation)