import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from sklearn.ensemble import IsolationForest
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

st.set_page_config(page_title="AEGIS Threat Intelligence", layout="wide")

# -------------------------------
# CYBERSECURITY UI
# -------------------------------

st.markdown("""
<style>

.stApp{
background-color:#0B0F19;
color:#E6EDF3;
}

h1,h2,h3{
color:#00FFC6;
}

div[data-testid="stMetric"]{
background:#161B22;
padding:20px;
border-radius:10px;
border:1px solid #30363d;
}

.stButton>button{
background:#00FFC6;
color:black;
font-weight:bold;
border-radius:8px;
}

.stDownloadButton>button{
background:#FF4D4D;
color:white;
border-radius:8px;
}

</style>
""", unsafe_allow_html=True)

st.title("AEGIS Financial Threat Intelligence Console")

st.markdown("AI-Driven Fraud Detection | Credit Risk | Behaviour Monitoring")

# -------------------------------
# DATA UPLOAD
# -------------------------------

uploaded_file = st.file_uploader("Upload Transaction Dataset", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.success("Dataset Loaded")

    st.write("Dataset Preview")
    st.dataframe(df.head())

    # -------------------------------
    # RUN ANALYSIS
    # -------------------------------

    if st.button("Run AEGIS Threat Analysis"):

        st.info("Running AI Threat Analysis...")

        # -------------------------------
        # DATA PREP
        # -------------------------------

        numeric_cols = df.select_dtypes(include=np.number).columns

        X = df[numeric_cols]

        # -------------------------------
        # BEHAVIOUR ANOMALY
        # -------------------------------

        iso = IsolationForest(contamination=0.02)

        df["anomaly"] = iso.fit_predict(X)

        behaviour_score = abs(df["anomaly"].mean())

        # -------------------------------
        # FRAUD MODEL
        # -------------------------------

        fraud_prob = 0

        if "fraud" in df.columns:

            y = df["fraud"]

            X_train, X_test, y_train, y_test = train_test_split(X, y)

            model = XGBClassifier()

            model.fit(X_train, y_train)

            fraud_prob = model.predict_proba(X_test)[:,1].mean()

        # -------------------------------
        # CREDIT RISK (simple heuristic)
        # -------------------------------

        credit_risk = X.mean().mean() / X.max().max()

        # -------------------------------
        # NETWORK RISK
        # -------------------------------

        network_risk = 0

        G = nx.Graph()

        if "customer" in df.columns and "merchant" in df.columns:

            fraud_df = df[df["fraud"]==1].head(100)

            for _,row in fraud_df.iterrows():

                G.add_edge(row["customer"],row["merchant"])

            network_risk = len(G.nodes)/100

        # -------------------------------
        # FINAL SCORE
        # -------------------------------

        final_score = np.mean([
        behaviour_score,
        fraud_prob,
        credit_risk,
        network_risk
        ])

        st.success("Analysis Complete")

        # -------------------------------
        # METRICS
        # -------------------------------

        col1,col2,col3,col4 = st.columns(4)

        col1.metric("Behaviour Risk", round(behaviour_score,3))
        col2.metric("Fraud Probability", round(fraud_prob,3))
        col3.metric("Credit Risk", round(credit_risk,3))
        col4.metric("Network Risk", round(network_risk,3))

        # -------------------------------
        # FINAL SCORE
        # -------------------------------

        st.subheader("Final Risk Score")

        st.error(round(final_score,3))

        # -------------------------------
        # TRANSACTION DISTRIBUTION
        # -------------------------------

        st.subheader("Transaction Distribution")

        if "amount" in df.columns:

            fig = px.histogram(df,x="amount")

            st.plotly_chart(fig,use_container_width=True)

        # -------------------------------
        # FRAUD NETWORK GRAPH
        # -------------------------------

        st.subheader("Fraud Network Graph")

        if len(G.nodes)>0:

            pos = nx.spring_layout(G)

            edge_x=[]
            edge_y=[]

            for edge in G.edges():
                x0,y0=pos[edge[0]]
                x1,y1=pos[edge[1]]
                edge_x.extend([x0,x1,None])
                edge_y.extend([y0,y1,None])

            edge_trace=go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1),
            hoverinfo='none',
            mode='lines')

            node_x=[]
            node_y=[]

            for node in G.nodes():
                x,y=pos[node]
                node_x.append(x)
                node_y.append(y)

            node_trace=go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers',
            marker=dict(size=10)
            )

            fig=go.Figure(data=[edge_trace,node_trace])

            st.plotly_chart(fig,use_container_width=True)

        else:
            st.warning("No fraud network connections detected")

        # -------------------------------
        # SUSPICIOUS TRANSACTIONS
        # -------------------------------

        st.subheader("Suspicious Transactions")

        suspicious = df[df["anomaly"]==-1]

        st.dataframe(suspicious.head(20))

        # -------------------------------
        # AI FRAUD INVESTIGATION
        # -------------------------------

        st.subheader("AI Fraud Investigation")

        if final_score > 0.6:

            st.error("""
High systemic financial risk detected.

Recommended actions:
• Freeze suspicious accounts
• Initiate enhanced KYC review
• Monitor merchant clusters
""")

        elif final_score > 0.3:

            st.warning("""
Moderate risk environment.

Recommended actions:
• Increase transaction monitoring
• Flag abnormal customers
""")

        else:

            st.success("""
Low systemic fraud risk detected.
Continue normal monitoring.
""")

        # -------------------------------
        # CAM REPORT GENERATOR
        # -------------------------------

        def generate_cam():

            buffer = BytesIO()

            doc = SimpleDocTemplate(buffer)

            styles = getSampleStyleSheet()

            story = []

            story.append(Paragraph("Credit Assessment Memorandum",styles['Title']))

            story.append(Spacer(1,20))

            story.append(Paragraph(f"Behaviour Risk: {behaviour_score}",styles['Normal']))
            story.append(Paragraph(f"Fraud Probability: {fraud_prob}",styles['Normal']))
            story.append(Paragraph(f"Credit Risk: {credit_risk}",styles['Normal']))
            story.append(Paragraph(f"Network Risk: {network_risk}",styles['Normal']))
            story.append(Paragraph(f"Final Risk Score: {final_score}",styles['Normal']))

            story.append(Spacer(1,20))

            story.append(Paragraph("Top Suspicious Transactions",styles['Heading2']))

            table_data=[list(suspicious.columns)]

            for i,row in suspicious.head(10).iterrows():
                table_data.append(list(row))

            table=Table(table_data)

            story.append(table)

            doc.build(story)

            buffer.seek(0)

            return buffer

        cam_pdf = generate_cam()

        st.download_button(
        label="Download CAM Report",
        data=cam_pdf,
        file_name="AEGIS_CAM_Report.pdf",
        mime="application/pdf"
        )