import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import calendar

# ========== CONFIGURACIÓN ==========
SHEET_ID = "1HRQo2fQyfJjB9RxIai9-1YfJQEFEXGW--Z2CrOdUPT0"
URL_FORM = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"

st.set_page_config(page_title="ParDuo", page_icon="😎", layout="wide")

@st.cache_data(ttl=60)
def cargar_datos():
    """Carga los datos desde Google Sheets"""
    try:
        df = pd.read_csv(URL_FORM)
        return df
    except Exception as e:
        st.sidebar.error(f"Error: {e}")
        return pd.DataFrame()

def crear_calendario(año, mes, df):
    """Crea calendario HTML con los gastos"""
    cal = calendar.monthcalendar(año, mes)
    nombre_mes = calendar.month_name[mes]
    
    # Extraer gastos por día
    gastos_por_dia = {}
    if not df.empty:
        for _, row in df.iterrows():
            try:
                fecha = pd.to_datetime(row['Fecha del movimiento'])
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

# ========== TÍTULO ==========
st.markdown("<h1 style='text-align:center;'>😎 ParDuo - Finanzas Jackson & Yuly</h1>", unsafe_allow_html=True)

# ========== CARGAR DATOS ==========
df = cargar_datos()

if df.empty:
    st.warning("⚠️ Aún no hay datos. Registra gastos en el formulario de Google.")
    st.stop()

# ========== MOSTRAR DATOS CRUDOS (para depuración) ==========
with st.expander("🔧 Ver datos crudos (solo para verificar)"):
    st.write("### Columnas encontradas:", list(df.columns))
    st.write("### Primeros registros:")
    st.dataframe(df.head())

# ========== SEPARAR INGRESOS Y GASTOS ==========
df_gastos = df[df['Tipo de movimiento'] == 'Gasto (pagas algo)']
df_ingresos = df[df['Tipo de movimiento'] == 'Ingreso (recibes dinero)']

total_gastos = df_gastos['Monto en soles (S/.)'].sum() if not df_gastos.empty else 0
total_ingresos = df_ingresos['Monto en soles (S/.)'].sum() if not df_ingresos.empty else 0

# ========== CREAR COLUMNAS ==========
col1, col2, col3, col4 = st.columns([1, 1, 1, 1.2])

with col1:
    st.markdown("### 📊 Resumen General")
    st.metric("💰 Ingresos", f"S/.{total_ingresos:,.2f}")
    st.metric("💸 Gastos", f"S/.{total_gastos:,.2f}")
    st.metric("📈 Balance", f"S/.{total_ingresos - total_gastos:,.2f}")

with col2:
    st.markdown("### 🎯 Presupuesto Personal (S/.300)")
    
    # Gastos personales Jackson (pregunta 7)
    gastos_jackson = df_gastos[df_gastos['Fondo de origen'] == 'Personal Jackson (S/.300 libre)']
    total_jackson = gastos_jackson['Monto en soles (S/.)'].sum() if not gastos_jackson.empty else 0
    
    # Gastos personales Yuly (pregunta 8)
    gastos_yuly = df_gastos[df_gastos['Fondo de origen'] == 'Personal Yuly (S/.300 libre)']
    total_yuly = gastos_yuly['Monto en soles (S/.)'].sum() if not gastos_yuly.empty else 0
    
    st.metric("Jackson", f"S/.{total_jackson:.2f} / S/.300")
    st.metric("Yuly", f"S/.{total_yuly:.2f} / S/.300")
    
    # Alertas si exceden presupuesto
    if total_jackson > 300:
        st.warning(f"⚠️ Jackson excedió su presupuesto en S/.{total_jackson - 300:.2f}")
    if total_yuly > 300:
        st.warning(f"⚠️ Yuly excedió su presupuesto en S/.{total_yuly - 300:.2f}")

with col3:
    st.markdown("### 🏠 Gastos del Hogar")
    
    # Gastos Variables (Jackson) - pregunta 9
    gastos_variables = df_gastos[df_gastos['Fondo de origen'] == 'Gastos Variables (Administra Jackson)']
    total_variables = gastos_variables['Monto en soles (S/.)'].sum() if not gastos_variables.empty else 0
    
    # Gastos Fijos (Yuly) - pregunta 10
    gastos_fijos = df_gastos[df_gastos['Fondo de origen'] == 'Gastos Fijos (Administra Yuly)']
    total_fijos = gastos_fijos['Monto en soles (S/.)'].sum() if not gastos_fijos.empty else 0
    
    st.metric("🛒 Gastos Variables (Jackson)", f"S/.{total_variables:,.2f}")
    st.metric("🏠 Gastos Fijos (Yuly)", f"S/.{total_fijos:,.2f}")

with col4:
    st.markdown("### 📅 Calendario de Gastos")
    hoy = datetime.now()
    
    # Mes anterior
    mes_ant = hoy.month - 1 if hoy.month > 1 else 12
    año_ant = hoy.year if hoy.month > 1 else hoy.year - 1
    st.markdown(crear_calendario(año_ant, mes_ant, df_gastos), unsafe_allow_html=True)
    
    # Mes actual
    st.markdown(crear_calendario(hoy.year, hoy.month, df_gastos), unsafe_allow_html=True)
    
    # Mes siguiente
    mes_sig = hoy.month + 1 if hoy.month < 12 else 1
    año_sig = hoy.year if hoy.month < 12 else hoy.year + 1
    st.markdown(crear_calendario(año_sig, mes_sig, df_gastos), unsafe_allow_html=True)

# ========== DETALLE DE GASTOS POR CATEGORÍA ==========
st.markdown("---")
st.markdown("### 📋 Detalle de gastos")

tab1, tab2, tab3, tab4 = st.tabs(["💰 Jackson Personal", "💰 Yuly Personal", "🛒 Variables", "🏠 Fijos"])

with tab1:
    if not gastos_jackson.empty:
        detalle = gastos_jackson.groupby('Gasto personal Jackson')['Monto en soles (S/.)'].sum().reset_index()
        detalle.columns = ['Categoría', 'Monto']
        st.dataframe(detalle, use_container_width=True)
        
        # Gráfico
        fig = px.pie(detalle, values='Monto', names='Categoría', title="Gastos Personales Jackson")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay gastos personales de Jackson aún")

with tab2:
    if not gastos_yuly.empty:
        detalle = gastos_yuly.groupby('Gasto personal Yuly')['Monto en soles (S/.)'].sum().reset_index()
        detalle.columns = ['Categoría', 'Monto']
        st.dataframe(detalle, use_container_width=True)
        
        fig = px.pie(detalle, values='Monto', names='Categoría', title="Gastos Personales Yuly")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay gastos personales de Yuly aún")

with tab3:
    if not gastos_variables.empty:
        detalle = gastos_variables.groupby('Gastos Variables Jackson')['Monto en soles (S/.)'].sum().reset_index()
        detalle.columns = ['Categoría', 'Monto']
        st.dataframe(detalle, use_container_width=True)
        
        fig = px.bar(detalle, x='Categoría', y='Monto', title="Gastos Variables")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay gastos variables aún")

with tab4:
    if not gastos_fijos.empty:
        detalle = gastos_fijos.groupby('Gastos Fijos Yuly')['Monto en soles (S/.)'].sum().reset_index()
        detalle.columns = ['Categoría', 'Monto']
        st.dataframe(detalle, use_container_width=True)
        
        fig = px.bar(detalle, x='Categoría', y='Monto', title="Gastos Fijos")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay gastos fijos aún")

# ========== ÚLTIMOS REGISTROS ==========
st.markdown("---")
st.markdown("### 📝 Últimos movimientos registrados")

columnas_mostrar = ['Fecha del movimiento', 'Persona responsable', 'Monto en soles (S/.)', 'Fondo de origen']
for col in ['Gasto personal Jackson', 'Gasto personal Yuly', 'Gastos Variables Jackson', 'Gastos Fijos Yuly']:
    if col in df.columns:
        columnas_mostrar.append(col)

df_mostrar = df[columnas_mostrar].copy()
df_mostrar.columns = ['Fecha', 'Responsable', 'Monto', 'Fondo', 'Detalle'] if len(columnas_mostrar) == 5 else columnas_mostrar
st.dataframe(df_mostrar.tail(10), use_container_width=True)

st.markdown("---")
st.caption("🔄 Los datos se actualizan cada 60 segundos automáticamente desde Google Forms")
st.caption("💡 Los días con fondo rojo en el calendario indican que hubo gastos")
