import streamlit as st
import requests

# Set the Flask API URL
FLASK_API_URL = "http://127.0.0.1:5000/predict"

# Streamlit UI
st.title("🛍️ AI-Powered Customer Segmentation")

st.markdown("Enter customer details below to predict their segment.")

# User input form
gender = st.selectbox("Gender", ["Male", "Female"])
city = st.selectbox("City", ["A", "B", "C"])
membership = st.selectbox("Membership Type", ["Gold", "Silver", "Bronze"])
satisfaction = st.selectbox("Satisfaction Level", ["High", "Medium", "Low"])

# Convert input to API-compatible format
input_data = {
    "Gender": 1 if gender == "Female" else 0,
    "City_A": 1 if city == "A" else 0,
    "City_B": 1 if city == "B" else 0,
    "City_C": 1 if city == "C" else 0,
    "Membership Type_Gold": 1 if membership == "Gold" else 0,
    "Membership Type_Silver": 1 if membership == "Silver" else 0,
    "Membership Type_Bronze": 1 if membership == "Bronze" else 0,
    "Satisfaction Level_High": 1 if satisfaction == "High" else 0,
    "Satisfaction Level_Medium": 1 if satisfaction == "Medium" else 0,
    "Satisfaction Level_Low": 1 if satisfaction == "Low" else 0,
}

# Submit button
if st.button("Predict Segment"):
    try:
        response = requests.post(FLASK_API_URL, json=input_data)
        result = response.json()

        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.success(f"Predicted Segment: **{result['Customer Segment']}**")

    except Exception as e:
        st.error(f"Request failed: {str(e)}")

