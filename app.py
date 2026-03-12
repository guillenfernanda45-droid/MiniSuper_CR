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

def ventas_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa las ventas por mes.

    Retorna un DataFrame con columnas: Año_Mes, Ventas
    Ordenado de manera cronologica.
    """
    df = df.copy()
    df["Año_Mes"] = pd.to_datetime(df["Fecha_Orden"]).dt.to_period("M").astype(str)
    return (
        df.groupby("Año_Mes")["Ventas"].sum()
        .reset_index().sort_values("Año_Mes")
        .round(2)
    )

def ventas_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa las ventas por categoria de producto.

    Retorna un DataFrame con columnas: Categoria, Ventas
    """
    return (
        df.groupby("Categoria")["Ventas"].sum()
        .reset_index().sort_values("Ventas", ascending=False)
        .round(2)
    )

def ventas_por_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa las ventas por region geografica.

    Retorna un DataFrame con columnas: Region, Ventas
    """
    return (
        df.groupby("Region")["Ventas"].sum()
        .reset_index().sort_values("Ventas", ascending=False)
        .round(2)
    )
df_base = cargar_datos()

st.title("📊 Análisis de Ventas Super Tienda CR")

st.sidebar.header("Filtros de búsqueda")
opciones = obtener_opciones(df_base)

filtro_años = st.sidebar.multiselect(
    ":blue[Seleccione Año(s):]", 
    opciones["años"], 
    default=opciones["años"]
)

filtro_cat = st.sidebar.multiselect(
    ":red[Categoría de Producto:]", 
    opciones["categorias"],
    default=opciones["categorias"]
)

filtro_reg = st.sidebar.multiselect(
    ":green[Región Geográfica:]",
    opciones["regiones"],
    default=opciones["regiones"]
)

df = filtrar_datos(df_base, años=filtro_años, categorias=filtro_cat, regiones=filtro_reg)

st.markdown("""
    <style>
    span[data-baseweb="tag"] {
        background-color: #2c2c2c !important;
        color: #FF4B4B !important;
        border: 1px solid #FF4B4B;
    }
    section[data-testid="stSidebar"] .stButton > button {
        font-size: 12px !important;
        padding: 2px 15px !important;
        min-height: 30px !important;
        width: auto !important;
        border: 2px solid #007bff !important; 
        color: #007bff !important;
        background-color: transparent;
        border-radius: 8px;
        transition: 0.3s;
    }
    section[data-testid="stSidebar"] .stButton > button:active {
        border-color: #28A745 !important;
        color: #28A745 !important;
        background-color: #fff5f5;
    }
    </style>
""", unsafe_allow_html=True)

resumen = calcular_resumen(df)
col1, col2, col3 = st.columns(3)

col1.metric("💰Ventas Totales", f"₡{resumen['ventas']:,.0f}", delta="10%")
col2.metric("📈Ganancia Total", f"₡{resumen['ganancia']:,.0f}", delta="10%")
col3.metric("📦Número de Órdenes", resumen['ordenes'], delta="10%")

st.subheader("Tendencia de Ventas Mensuales")
datos_mes = ventas_por_mes(df)
st.line_chart(datos_mes, x="Año_Mes", y="Ventas", color="#FF0000")

col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Ventas por Categoría")
    datos_cat = ventas_por_categoria(df)
    st.bar_chart(datos_cat, x="Categoria", y="Ventas", color="#008000")

with col_der:
    st.subheader("Distribución por Región")
    datos_reg = ventas_por_region(df)
    st.bar_chart(datos_reg, x="Region", y="Ventas", color="#0000FF")

st.subheader("📊 Tabla de datos")
st.dataframe(df, use_container_width=True, hide_index=True)