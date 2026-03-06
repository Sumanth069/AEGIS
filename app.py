import streamlit as st
from engine.risk_engine import generate_report
import tempfile

st.title("AEGIS AI Risk Intelligence System")

st.write("Bank Officer Loan Risk Analysis")

name = st.text_input("Customer Name")

loan = st.number_input("Loan Amount")

transactions = st.file_uploader("Upload Transaction CSV")

if st.button("Analyze Customer"):

    if transactions is not None:

        temp = tempfile.NamedTemporaryFile(delete=False)

        temp.write(transactions.read())

        report = generate_report(
            name,
            loan,
            temp.name
        )

        st.subheader("Risk Intelligence Report")

        st.write("Behaviour Risk:", report["behaviour_risk"])
        st.write("Credit Risk:", report["credit_risk"])
        st.write("Network Risk:", report["network_risk"])
        st.write("Default Probability:", report["default_probability"])

        st.subheader("Final Risk Score")

        st.write(report["final_risk"])

        st.subheader("Recommendation")

        st.success(report["recommendation"])

        st.subheader("AI Investigation Report")

        st.info(report["explanation"])