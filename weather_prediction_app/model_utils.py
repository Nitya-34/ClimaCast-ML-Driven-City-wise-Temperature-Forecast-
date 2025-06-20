import pickle
import pandas as pd
import streamlit as st
from joblib import load


@st.cache_resource
def load_models():
    return {
        "XGBoost": pickle.load(open("weather_prediction_app/models/xgb_model.pkl", "rb")),
        "Random Forest": load("weather_prediction_app/models/rf_model.joblib"),
        "Linear Regression": pickle.load(open("weather_prediction_app/models/lr_model.pkl", "rb")),
        "SVR": pickle.load(open("weather_prediction_app/models/svr_model.pkl", "rb"))
    }

def make_prediction(model, input_df):
    return model.predict(input_df)[0]
