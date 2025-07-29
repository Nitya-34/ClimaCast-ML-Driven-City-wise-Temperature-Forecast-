import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import time
import plotly.graph_objects as go
import plotly.colors as pc
from model_utils import load_models, make_prediction


# ==== UI Header ====
st.set_page_config(page_title="Weather Prediction App", layout="centered")
st.image("weather_prediction_app/assets/logo.png", width=100)  # Optional logo
st.title("🌤️ Smart Weather Forecasting")
st.markdown("Predict short-term temperature using ML models trained on multi-city historical data.")
# 🧭 Sidebar instruction
st.markdown("🌈 **Click the arrow in the top-left corner👈 to open the sidebar and input your weather parameters☁️.**")

# ==== Load models ====
models = load_models()

# ==== City map (must match training encoder) ====
city_map = {
    "Bangalore": 0,
    "Bhubhneshwar": 1,
    "Chennai": 2,
    "Delhi": 3,
    "Lucknow": 4,
    "Mumbai": 5,
    "Rajasthan": 6,
}

# ==== Sidebar for input ====
st.sidebar.header("📥 Input Parameters")
model_name = st.sidebar.selectbox("Model", list(models.keys()))
city = st.sidebar.selectbox("City", list(city_map.keys()))
date_input = st.sidebar.date_input("Date", datetime.date.today())

# Keep sliders for tmin and tmax
tmin = st.sidebar.slider("Min Temperature (°C)", 10.0, 40.0, 25.0)
tmax = st.sidebar.slider("Max Temperature (°C)", 20.0, 50.0, 35.0)

# Use number_input for precipitation
prcp = st.sidebar.number_input("Precipitation (mm)", min_value=0.0, max_value=200.0, value=0.0, step=0.1)

#==== Predict ======================
if st.sidebar.button("🔍 Predict"):
    # ✅ Prepare input
    input_df = pd.DataFrame([{
        "tmin": tmin,
        "tmax": tmax,
        "prcp": prcp,
        "city": city_map[city],
        "month": date_input.month,
        "day": date_input.day
    }])

    # ✅ Get selected model and predict
    model = models[model_name]
    prediction = model.predict(input_df)[0]

   #============== Visualisation =================================   
    
    # 1️⃣ Show result first
    st.subheader("📊 Prediction Result")
    st.metric("Predicted Avg Temperature", f"{prediction:.2f} °C")
  
    # Define the color scale
    colorscale = "RdYlBu_r"  # reversed RdYlBu: blue → red

    # Normalize temperature to a 0–1 scale for color sampling (assuming temp range 10–50°C)
    def normalize_temp(temp, min_val=10, max_val=50):
        return min(max((temp - min_val) / (max_val - min_val), 0), 1)
    
    normalized_temp = normalize_temp(prediction)
    bar_color = pc.sample_colorscale(colorscale, normalized_temp)[0]  # Exact tip color
    
    # 🎯 Thermometer-style bar chart
    fig = go.Figure(go.Bar(
        x=[prediction],
        y=["Predicted Temp (°C)"],
        orientation='h',
        text=[f"{prediction:.2f}°C"],
        textposition='auto',
        marker=dict(
            color=bar_color           
        )
    ))
    
    # 🎨 Add color strip below the bar (from 10 to 50°C)
    num_segments = 40
    for i in range(num_segments):
        x0 = 10 + i
        x1 = 10 + i + 1
        norm_val = i / num_segments  # normalize to [0,1]
        color = pc.sample_colorscale(colorscale, norm_val)[0]
    
        fig.add_shape(
            type="rect",
            x0=x0,
            x1=x1,
            y0=-0.6,
            y1=-0.4,
            line=dict(width=0),
            fillcolor=color,
            layer="below"
        )
    
    # Chart layout
    fig.update_layout(
        xaxis=dict(range=[10, 50], title="Temperature (°C)"),
        title="🌡️ Temperature Prediction with Color Strip",
        height=250,
        margin=dict(t=40, b=40)
    )
    
    # Show the chart
    st.plotly_chart(fig, use_container_width=True)
    
    # 😎 Emoji temperature interpretation
    def get_temp_emoji(temp):
        if temp < 15:
            return "🥶 Very Cold, Wear Scarfs 🧣🧥!"
        elif temp < 25:
            return "🌤️ Mild, Can go for a walk 🤗!"
        elif temp < 35:
            return " Drink plenty of water 🚰 and stay in shade🌳!"
        elif temp < 42:
            return "Avoid outdoor activities🎮 and stay in a cool place🏠!"
        else:
            return "♨️ Scorching, Stay Inside!!"
    
    # Show the result
    st.markdown(f"### {get_temp_emoji(prediction)} — {prediction:.2f}°C")
