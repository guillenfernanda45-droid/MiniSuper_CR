import streamlit as st
import pandas as pd

st.set_page_config(page_title="Super Tienda CR", layout="wide")

def cargar_datos():
    df = pd.read_csv("supertienda_cr.csv")
    df["Fecha_Orden"] = pd.to_datetime(df["Fecha_Orden"])
    df["Año"] = df["Fecha_Orden"].dt.year
    return df