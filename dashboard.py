import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import calendar

# ========== CONFIGURACIÓN ==========
SHEET_ID = "1HRQo2fQyfJjB9RxIai9-1YfJQEFEXGW--Z2CrOdUPT0"
URL_FORM = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

st.set_page_config(page_title="ParDuo", page_icon="💑", layout="wide")

@st.cache_data(ttl=60)
def cargar_datos():
    try:
        df = pd.read_csv(URL_FORM)
        return df
    except:
        return pd.DataFrame()

def crear_calendario(año, mes, df):
    cal = calendar.monthcalendar(año, mes)
    nombre_mes = calendar.month_name[mes]
    
    # Extraer gastos por día
    gastos_por_dia = {}
    if not df.empty:
        for _, row in df.iterrows():
            try:
                fecha = pd.to_datetime(row.get('Fecha del movimiento', ''))
                if fecha.month == mes and fecha.year == año:
                    dia = fecha.day
                    monto = float(row['Monto en soles (S/.)'])
                    gastos_por_dia[dia] = gastos_por_dia.get(dia, 0) + monto
            except:
                pass
    
    html = f'<div style="background:#1e3c72; border-radius:15px; padding:15px; margin:10px 0; color:white;"><h4 style="text-align:center;">{nombre_mes} {año}</h4><table style="width:100%; text-align:center;">'
    for semana in cal:
        html += "<tr>"
        for dia in semana:
            if dia == 0:
                html += "<td style='color:#666;'>-</td>"
            else:
                tiene_gasto = dia in gastos_por_dia
                estilo = "background:#FF4444; border-radius:50%;" if tiene_gasto else ""
                html += f"<td style='padding:8px;{estilo}'>{dia}</td>"
        html += "</tr>"
    html += "</table></div>"
    return html

# Título
st.markdown("<h1 style='text-align:center;'>💑 ParDuo - Finanzas Jackson & Yuly</h1>", unsafe_allow_html=True)

df = cargar_datos()

if df.empty:
    st.warning("⚠️ Aún no hay datos. Registra gastos en el formulario de Google.")
    st.stop()

# Separar gastos e ingresos
df_gastos = df[df['Tipo de movimiento'] == 'Gasto (pagas algo)']
df_ingresos = df[df['Tipo de movimiento'] == 'Ingreso (recibes dinero)']

total_gastos = df_gastos['Monto en soles (S/.)'].sum() if not df_gastos.empty else 0
total_ingresos = df_ingresos['Monto en soles (S/.)'].sum() if not df_ingresos.empty else 0

col1, col2, col3, col4 = st.columns([1, 1, 1, 1.2])

with col1:
    st.metric("💰 Ingresos", f"S/.{total_ingresos:,.2f}")
    st.metric("💸 Gastos", f"S/.{total_gastos:,.2f}")
    st.metric("📈 Balance", f"S/.{total_ingresos - total_gastos:,.2f}")

with col2:
    gastos_jackson = df_gastos[df_gastos['Fondo de origen'] == 'Personal Jackson (S/.300 libre)']
    gastos_yuly = df_gastos[df_gastos['Fondo de origen'] == 'Personal Yuly (S/.300 libre)']
    total_jackson = gastos_jackson['Monto en soles (S/.)'].sum() if not gastos_jackson.empty else 0
    total_yuly = gastos_yuly['Monto en soles (S/.)'].sum() if not gastos_yuly.empty else 0
    st.metric("Jackson Personal", f"S/.{total_jackson:.2f} / S/.300")
    st.metric("Yuly Personal", f"S/.{total_yuly:.2f} / S/.300")

with col3:
    gastos_variables = df_gastos[df_gastos['Fondo de origen'] == 'Gastos Variables (Administra Jackson)']
    gastos_fijos = df_gastos[df_gastos['Fondo de origen'] == 'Gastos Fijos (Administra Yuly)']
    total_variables = gastos_variables['Monto en soles (S/.)'].sum() if not gastos_variables.empty else 0
    total_fijos = gastos_fijos['Monto en soles (S/.)'].sum() if not gastos_fijos.empty else 0
    st.metric("🛒 Gastos Variables", f"S/.{total_variables:,.2f}")
    st.metric("🏠 Gastos Fijos", f"S/.{total_fijos:,.2f}")

with col4:
    st.markdown("### 📅 Calendario")
    hoy = datetime.now()
    st.markdown(crear_calendario(hoy.year, hoy.month, df_gastos), unsafe_allow_html=True)

st.markdown("---")
st.caption("Los datos se actualizan cada 60 segundos automáticamente desde Google Forms")