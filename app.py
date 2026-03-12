import streamlit as st
import pandas as pd

st.set_page_config(page_title="Super Tienda CR", layout="wide")

def cargar_datos():
    df = pd.read_csv("supertienda_cr.csv")
    df["Fecha_Orden"] = pd.to_datetime(df["Fecha_Orden"])
    df["Año"] = df["Fecha_Orden"].dt.year
    return df

def calcular_resumen(df: pd.DataFrame) -> dict:
    """
    Calcula un resumen general de los datos.

    Retorna un diccionario con:
        "ventas"   -> float, suma total de ventas
        "ganancia" -> float, suma total de ganancia
        "ordenes"  -> int, cantidad de ordenes unicas
    """
    return {
        "ventas": round(df["Ventas"].sum(), 2),
        "ganancia": round(df["Ganancia"].sum(), 2),
        "ordenes": df["ID_Orden"].nunique(),
    }