import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Simulate PPG signal processing and BP estimation
def simulate_ppg_and_estimate_bp():
    # Generate a simulated PPG signal
    time = np.linspace(0, 5, 500)
    ppg_signal = np.sin(2 * np.pi * 1.2 * time) + 0.5 * np.sin(2 * np.pi * 2.4 * time)
    ppg_signal += np.random.normal(0, 0.1, ppg_signal.shape)

    # Simulate BP estimation (in a real app, this would involve complex signal processing)
    systolic = np.random.randint(100, 160)
    diastolic = np.random.randint(60, 100)
    
    return ppg_signal, time, systolic, diastolic

def analyze_bp(systolic, diastolic):
    if systolic >= 180 or diastolic >= 120:
        return "Hypertensive Crisis", "red"
    elif systolic >= 140 or diastolic >= 90:
        return "High Blood Pressure", "orange"
    elif systolic >= 120 or diastolic >= 80:
        return "Elevated", "yellow"
    else:
        return "Normal", "green"

# Initialize session state
if 'readings' not in st.session_state:
    st.session_state.readings = pd.DataFrame(columns=['Timestamp', 'Systolic', 'Diastolic', 'Status'])

st.title("Smartphone PPG-based Blood Pressure Monitoring - Ghana")

st.write("""
This app simulates a smartphone-based blood pressure monitoring system using photoplethysmography (PPG).
Place your finger on your phone's camera to measure your blood pressure (simulated in this demo).
""")

if st.button("Measure Blood Pressure"):
    with st.spinner("Processing PPG signal..."):
        # Simulate PPG measurement and BP estimation
        ppg_signal, time, systolic, diastolic = simulate_ppg_and_estimate_bp()
        
        # Analyze BP
        status, color = analyze_bp(systolic, diastolic)
        
        # Display results
        st.success("Measurement complete!")
        st.write(f"Systolic: {systolic} mmHg")
        st.write(f"Diastolic: {diastolic} mmHg")
        st.write(f"Status: {status}")
        
        # Plot PPG signal
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time, y=ppg_signal, mode='lines', name='PPG Signal'))
        fig.update_layout(title="Simulated PPG Signal", xaxis_title="Time (s)", yaxis_title="Amplitude")
        st.plotly_chart(fig)
        
        # Save reading
        new_reading = pd.DataFrame({
            'Timestamp': [datetime.now()],
            'Systolic': [systolic],
            'Diastolic': [diastolic],
            'Status': [status]
        })
        st.session_state.readings = pd.concat([st.session_state.readings, new_reading], ignore_index=True)

# Display history and trends
if not st.session_state.readings.empty:
    st.subheader("Measurement History")
    st.dataframe(st.session_state.readings)
    
    st.subheader("Blood Pressure Trend")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=st.session_state.readings['Timestamp'], y=st.session_state.readings['Systolic'], mode='lines+markers', name='Systolic'))
    fig.add_trace(go.Scatter(x=st.session_state.readings['Timestamp'], y=st.session_state.readings['Diastolic'], mode='lines+markers', name='Diastolic'))
    fig.update_layout(title="Blood Pressure Trend", xaxis_title="Time", yaxis_title="Blood Pressure (mmHg)")
    st.plotly_chart(fig)

# Telemedicine Integration
st.subheader("Telemedicine Integration")
if st.button("Connect with a Healthcare Provider"):
    st.info("Connecting you with a healthcare provider... (This would initiate a telemedicine consultation in a real app)")

# Health Tips
st.subheader("Health Tips")
tips = [
    "Stay hydrated! Aim for 8 glasses of water a day.",
    "Reduce salt intake in your diet.",
    "Exercise regularly - even a 30-minute walk can help.",
    "Manage stress through deep breathing or meditation.",
    "Eat more fruits and vegetables, especially those locally grown in Ghana.",
    "Limit alcohol consumption and avoid smoking.",
    "Take your medication as prescribed by your healthcare provider.",
    "Get adequate sleep - aim for 7-9 hours per night."
]
st.info(tips[len(st.session_state.readings) % len(tips)])

# Local Resources
st.subheader("Local Health Resources in Ghana")
resources = {
    "Ghana Health Service": "Visit https://www.ghanahealthservice.org/ for official health information",
    "Telemedicine Services": "Check with your local health center for available telemedicine options",
    "Community Health Workers": "Contact your local CHPS compound for support",
    "Healthy Eating": "Visit your local market for fresh, locally grown produce",
    "Exercise Groups": "Join community exercise groups in your area for support and motivation"
}
for resource, info in resources.items():
    st.write(f"- {resource}: {info}")
