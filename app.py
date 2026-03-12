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

def filtrar_datos(df, años=None, categorias=None, regiones=None):
    """
    Filtra el DataFrame segun los parametros indicados.
    Si un parametro es None, no aplica ese filtro.

    Parametros:
        df: DataFrame original
        años: lista de enteros, por ejemplo [2023, 2024]
        categorias: lista de strings, por ejemplo ["Tecnologia"]
        regiones: lista de strings, por ejemplo ["Central"]

    Retorna un DataFrame filtrado.
    """
    resultado = df.copy()
    if años:
        resultado = resultado[resultado["Año"].isin(años)]
    if categorias:
        resultado = resultado[resultado["Categoria"].isin(categorias)]
    if regiones:
        resultado = resultado[resultado["Region"].isin(regiones)]
    return resultado

def obtener_opciones(df: pd.DataFrame) -> dict:
    """
    Retorna un diccionario con las opciones unicas para los filtros.

    Llaves: "años", "categorias", "regiones"
    Cada una contiene una lista ordenada.
    """
    return {
        "años": sorted(df["Año"].unique().tolist()),
        "categorias": sorted(df["Categoria"].unique().tolist()),
        "regiones": sorted(df["Region"].unique().tolist()),
    }

