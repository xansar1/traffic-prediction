import streamlit as st
import requests
import pandas as pd

# Replace with your Render backend URL when deployed
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Traffic Prediction Dashboard", layout="wide")
st.title("🚦 Real-Time Traffic Prediction")

# Health Check
try:
    health = requests.get(f"{BACKEND_URL}/health").json()
    st.success(f"Backend Status: {health['status']}")
except:
    st.error("⚠️ Could not connect to backend. Start backend first!")

# Input Form
st.subheader("📊 Enter Traffic Prediction Data")
with st.form("prediction_form"):
    segment_id = st.text_input("Road Segment ID", "A1")
    horizon = st.number_input("Horizon (minutes)", min_value=1, max_value=120, value=15)
    speed = st.number_input("Predicted Speed (km/h)", min_value=0, max_value=200, value=60)
    model = st.text_input("Model Used", "LSTM")
    submit = st.form_submit_button("Submit Prediction")

if submit:
    payload = {
        "segment_id": segment_id,
        "horizon_min": horizon,
        "predicted_speed": speed,
        "model": model
    }
    try:
        res = requests.post(f"{BACKEND_URL}/predict", json=payload)
        if res.status_code == 200:
            st.success("✅ Prediction submitted successfully!")
        else:
            st.error("❌ Failed to submit prediction")
    except:
        st.error("⚠️ Could not connect to backend")

# Show Saved Predictions
st.subheader("📈 Stored Predictions")
try:
    res = requests.get(f"{BACKEND_URL}/predictions").json()
    if res:
        df = pd.DataFrame(res)
        st.dataframe(df)
    else:
        st.info("No predictions available yet.")
except:
    st.error("⚠️ Could not fetch predictions. Start backend first!")
