import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest, RandomForestClassifier

# Page setup
st.set_page_config(page_title="Cyber Threat Detection", layout="wide")

st.title("🔐 Cyber Threat Detection System")

# Load dataset
try:
    df = pd.read_csv("dataset.csv")
except:
    st.error("dataset.csv not found! Make sure it is in the same folder.")
    st.stop()

# Show raw data
st.subheader("Raw Data")
st.write(df)

# Convert text to numbers
df['access_level'] = df['access_level'].map({
    'user': 0,
    'admin': 1,
    'root': 2
})

# Features & labels
X = df[['bytes', 'failed_logins', 'access_level']]
y = df['label']

# Anomaly Detection
anomaly_model = IsolationForest(contamination=0.2)
df['anomaly'] = anomaly_model.fit_predict(X)

# Intent Prediction
intent_model = RandomForestClassifier()
intent_model.fit(X, y)
df['intent'] = intent_model.predict(X)

# Final Decision
def final_decision(row):
    if row['anomaly'] == -1 or row['intent'] == 1:
        return "THREAT"
    return "NORMAL"

df['final'] = df.apply(final_decision, axis=1)

# Explanation
def explain(row):
    if row['failed_logins'] > 3:
        return "High failed logins (Brute force attack)"
    elif row['bytes'] > 3000:
        return "Large data transfer (Possible data leak)"
    else:
        return "Normal behavior"

df['reason'] = df.apply(explain, axis=1)

# Dashboard metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Records", len(df))

with col2:
    threats = df[df['final'] == "THREAT"].shape[0]
    st.metric("Threats Detected", threats)

# Highlight colors
def highlight(row):
    if row['final'] == "THREAT":
        return ['background-color: #ff4d4d'] * len(row)
    else:
        return ['background-color: #4dff88'] * len(row)

# Show results
st.subheader("Detection Results")
st.dataframe(
    df[['bytes', 'failed_logins', 'final', 'reason']]
    .style.apply(highlight, axis=1)
)

# Explanation section
st.subheader("About the System")
st.write("""
This system uses:
- Isolation Forest for anomaly detection
- Random Forest for threat classification
- Rule-based logic to combine results

It detects suspicious behavior like:
- High login failures
- Unusual data transfer
""")