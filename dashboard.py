import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ========== CONFIGURACIÓN ==========
SHEET_ID = "1HRQo2fQyfJjB9RxIai9-1YfJQEFEXGW--Z2CrOdUPT0"
URL_DATA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=3_Dashboard_Data"

st.set_page_config(page_title="ParDuo", page_icon="😎", layout="wide")

@st.cache_data(ttl=60)
def cargar_datos():
    try:
        df = pd.read_csv(URL_DATA)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# ========== TÍTULO ==========
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px;">
    <h1 style="color: white; margin: 0;">😎 ParDuo</h1>
    <p style="color: white; margin: 10px 0 0 0;">Finanzas Jackson & Yuly</p>
</div>
""", unsafe_allow_html=True)

# ========== CARGAR DATOS ==========
df = cargar_datos()

if df.empty:
    st.warning("⚠️ Cargando datos... Verifica que la hoja sea pública")
    st.stop()

# Convertir a diccionario (asumiendo columnas A y B)
datos = {}
for _, row in df.iterrows():
    if len(row) >= 2:
        clave = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
        valor = row.iloc[1] if pd.notna(row.iloc[1]) else 0
        if clave:
            datos[clave] = valor

# ========== KPI CARDS ==========
st.markdown("### 📊 Resumen General")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Dinero Acumulado", f"S/.{datos.get('Dinero Acumulado', 0):,.2f}")
with col2:
    st.metric("📈 Dinero Invertido", f"S/.{datos.get('Dinero invertido', 0):,.2f}")
with col3:
    st.metric("🛒 Gastos Variables", f"S/.{datos.get('📂 Gastos Variables Jackson', 0):,.2f}")
with col4:
    st.metric("🏠 Gastos Fijos", f"S/.{datos.get('📂 Gastos Fijos Yuly', 0):,.2f}")

st.markdown("---")

# ========== PRESUPUESTOS PERSONALES ==========
st.markdown("### 🎯 Presupuesto Personal (S/.300 c/u)")

col1, col2 = st.columns(2)

jackson_gasto = datos.get('📂 Gasto personal Jackson', 0)
jackson_restante = datos.get('Presupuesto personal – Jackson', 300) - jackson_gasto
with col1:
    st.metric("Jackson", f"S/.{jackson_gasto:.2f}", delta=f"Restan S/.{jackson_restante:.2f}")
    st.progress(min(1.0, jackson_gasto / 300))

yuly_gasto = datos.get('📂 Gasto personal Yuly', 0)
yuly_restante = datos.get('Presupuesto personal – Yuly', 300) - yuly_gasto
with col2:
    st.metric("Yuly", f"S/.{yuly_gasto:.2f}", delta=f"Restan S/.{yuly_restante:.2f}")
    st.progress(min(1.0, yuly_gasto / 300))

st.markdown("---")

# ========== GRÁFICO DE GASTOS ==========
st.markdown("### 📊 Distribución de Gastos")

gastos_data = pd.DataFrame({
    'Categoría': ['Jackson Personal', 'Yuly Personal', 'Gastos Variables', 'Gastos Fijos'],
    'Monto': [
        jackson_gasto,
        yuly_gasto,
        datos.get('📂 Gastos Variables Jackson', 0),
        datos.get('📂 Gastos Fijos Yuly', 0)
    ]
})

fig = px.pie(gastos_data, values='Monto', names='Categoría', 
             title="Gastos por Categoría",
             color_discrete_sequence=['#667eea', '#764ba2', '#4ECDC4', '#FF6B6B'])
st.plotly_chart(fig, use_container_width=True)

# ========== TABLA DE GASTOS FIJOS (Leyenda) ==========
st.markdown("### 🏠 Desglose Gastos Fijos")

# Buscar columnas de leyenda en el DataFrame
gastos_fijos_df = df[df.iloc[:, 0].astype(str).str.contains('Luz|Agua|Router|Plan celular|Préstamo|Almacenamiento', na=False)]
if not gastos_fijos_df.empty:
    st.dataframe(gastos_fijos_df.iloc[:, :2], use_container_width=True)

st.markdown("---")
st.caption("🔄 Datos actualizados cada 60 segundos desde Google Sheets")
