import pickle
import pandas as pd
import streamlit as st

@st.cache_resource
def load_models():
    return {
        "XGBoost": pickle.load(open("models/xgb_model.pkl", "rb")),
        "Random Forest": pickle.load(open("models/rf_model.pkl", "rb")),
        "Linear Regression": pickle.load(open("models/lr_model.pkl", "rb")),
        "SVR": pickle.load(open("models/svr_model.pkl", "rb"))
    }

def make_prediction(model, input_df):
    return model.predict(input_df)[0]
