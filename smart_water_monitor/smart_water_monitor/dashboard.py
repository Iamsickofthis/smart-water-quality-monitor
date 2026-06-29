import streamlit as st
import pandas as pd
import joblib

# Load trained AI model
model = joblib.load("water_quality_model.pkl")

st.title("💧 Smart Water Quality Monitor")

st.write("Enter water values and click Analyze")

# Inputs
ph = st.number_input("pH", value=7.0)

hardness = st.number_input("Hardness", value=200.0)

solids = st.number_input("Solids", value=18000.0)

turbidity = st.number_input("Turbidity", value=3.0)

if st.button("Analyze Water"):

    sample = pd.DataFrame([{
        "ph": ph,
        "Hardness": hardness,
        "Solids": solids,
        "Chloramines": 7,
        "Sulfate": 330,
        "Conductivity": 400,
        "Organic_carbon": 12,
        "Trihalomethanes": 70,
        "Turbidity": turbidity
    }])

    prediction = model.predict(sample)

    if prediction[0] == 1:
        st.success("🟢 Safe Water")
    else:
        st.error("🔴 Unsafe Water")