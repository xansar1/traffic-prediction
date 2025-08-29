import streamlit as st
import requests
import pandas as pd
import time

API_URL = "https://traffic-backend.onrender.com"

st.set_page_config(page_title="Traffic Prediction Dashboard", layout="wide")

st.title("🚦 Real-Time Traffic Prediction Dashboard")

# Health Check
try:
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200:
        st.success("✅ Backend is running")
    else:
        st.error("❌ Backend not available")
except:
    st.error("⚠️ Could not connect to backend. Start backend.ipynb first!")

# Input Form
st.subheader("Add New Prediction")
with st.form("prediction_form"):
    segment_id = st.text_input("Road Segment ID", "A1")
    horizon_min = st.slider("Prediction Horizon (minutes)", 5, 120, 30)
    predicted_speed = st.number_input("Predicted Speed (km/h)", 0, 200, 60)
    model = st.selectbox("Model Used", ["LSTM", "ARIMA", "XGBoost"])
    submitted = st.form_submit_button("Submit")

    if submitted:
        payload = {
            "segment_id": segment_id,
            "horizon_min": horizon_min,
            "predicted_speed": predicted_speed,
            "model": model
        }
        res = requests.post(f"{API_URL}/predict", json=payload)
        if res.status_code == 200:
            st.success("✅ Prediction stored successfully")
        else:
            st.error("❌ Error storing prediction")

# Display Predictions
st.subheader("Stored Predictions")
try:
    res = requests.get(f"{API_URL}/predictions")
    if res.status_code == 200:
        data = res.json()
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)

            # Graph
            st.line_chart(df.set_index("timestamp")["predicted_speed"])
        else:
            st.info("No predictions yet")
except Exception as e:
    st.error(f"Error fetching predictions: {e}")
