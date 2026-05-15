import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ========== CONFIGURACIÓN PARA JALAR DATOS DE GOOGLE SHEETS → ID + HOJAS DE INTERES==========
SHEET_ID = "1HRQo2fQyfJjB9RxIai9-1YfJQEFEXGW--Z2CrOdUPT0"

URL_HOJA_1 = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=1_Formulario_RAW"
URL_HOJA_3 = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=3_Dashboard_Data"

st.set_page_config(page_title="ParDuo", page_icon="😎", layout="wide")

@st.cache_data(ttl=60)
def formulario_raw():
    try:
        df = pd.read_csv(URL_HOJA_1)
        return df
    except Exception as e:
        st.error(f"Error cargando formulario_raw: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def dashboard_data():
    try:
        df = pd.read_csv(URL_HOJA_3)
        return df
    except Exception as e:
        st.error(f"Error cargando dashboard_data: {e}")
        return pd.DataFrame()

# ========== TÍTULO DE LA PAGINA DEL DASHBOARD ==========
st.markdown("""
    <h1 style="color: black; 
               margin-top: -65px; 
               text-align: center; 
               font-size: 30px; 
               font-family: 'Segoe UI'; 
               text-shadow: 3px 3px 5px rgba(0,0,0,0.4); 
               letter-spacing: 1px">
        😎 ParDuo
    </h1>
""", unsafe_allow_html=True)

# ========== CARGAR DATOS DE LA HOJA 1 & 3 DE GOOGLE SHEETS==========
df_raw = formulario_raw()
df_dash = dashboard_data()

if df_raw.empty:
    st.warning("⚠️ Cargando datos del formulario...")
if df_dash.empty:
    st.warning("⚠️ Cargando datos del dashboard...")

# ========== EXTRAER VALORES DE LA HOJA 3_Dashboard_Data POR POSICIÓN==========
# ========== EXTRAER VALORES DE LA HOJA 3_Dashboard_Data ==========
if not df_dash.empty:
    # Función para limpiar valores
    def limpiar_valor(valor):
        try:
            if pd.isna(valor):
                return 0
            valor_str = str(valor).replace("S/.", "").replace(",", "").strip()
            return float(valor_str) if valor_str else 0
        except:
            return 0
    
    # Extraer valores por posición
    num_filas = len(df_dash)
    num_cols = len(df_dash.columns)
    
    if num_filas > 7:
        gastado_jackson = limpiar_valor(df_dash.iloc[7, 1] if num_cols > 1 else 0)
        gastado_yuly = limpiar_valor(df_dash.iloc[8, 1] if num_cols > 1 else 0)
        gastado_variables = limpiar_valor(df_dash.iloc[9, 1] if num_cols > 1 else 0)
        gastado_fijos = limpiar_valor(df_dash.iloc[10, 1] if num_cols > 1 else 0)
        dinero_acumulado = limpiar_valor(df_dash.iloc[14, 1] if num_cols > 1 else 0)
        dinero_invertido = limpiar_valor(df_dash.iloc[15, 1] if num_cols > 1 else 0)
        presupuesto_jackson_total = limpiar_valor(df_dash.iloc[16, 1] if num_cols > 1 else 0)
        presupuesto_yuly_total = limpiar_valor(df_dash.iloc[17, 1] if num_cols > 1 else 0)
        gastos_variables_base = limpiar_valor(df_dash.iloc[18, 1] if num_cols > 1 else 0)
        gastos_fijos_base = limpiar_valor(df_dash.iloc[19, 1] if num_cols > 1 else 0)
    else:
        gastado_jackson = gastado_yuly = gastado_variables = gastado_fijos = 0
        dinero_acumulado = dinero_invertido = 12000
        presupuesto_jackson_total = presupuesto_yuly_total = 300
        gastos_variables_base = gastos_fijos_base = 0

else:
    gastado_jackson = gastado_yuly = gastado_variables = gastado_fijos = 0
    dinero_acumulado = dinero_invertido = 12000
    presupuesto_jackson_total = presupuesto_yuly_total = 300
    gastos_variables_base = gastos_fijos_base = 0

# ========== 💰 VALORES EXTRAÍDOS (AL PRINCIPIO) ==========
st.markdown("---")
st.subheader("💰 Valores extraídos de Google Sheets")

col1, col2 = st.columns(2)

with col1:
    st.metric("💰 Dinero Acumulado", f"S/.{dinero_acumulado:,.2f}")
    st.metric("📈 Dinero Invertido", f"S/.{dinero_invertido:,.2f}")
    st.metric("🎯 Presupuesto Jackson", f"S/.{presupuesto_jackson_total:,.2f}")
    st.metric("🎯 Presupuesto Yuly", f"S/.{presupuesto_yuly_total:,.2f}")

with col2:
    st.metric("👤 Gastado Jackson", f"S/.{gastado_jackson:,.2f}")
    st.metric("👤 Gastado Yuly", f"S/.{gastado_yuly:,.2f}")
    st.metric("🛒 Gastos Variables", f"S/.{gastado_variables:,.2f}")
    st.metric("🏠 Gastos Fijos", f"S/.{gastado_fijos:,.2f}")

# ========== PORCENTAJES ==========
if presupuesto_jackson_total > 0:
    porcentaje_jackson = (gastado_jackson / presupuesto_jackson_total) * 100
    restante_jackson = presupuesto_jackson_total - gastado_jackson
    st.caption(f"📊 Jackson: {porcentaje_jackson:.1f}% usado - Restante: S/.{restante_jackson:.2f}")

if presupuesto_yuly_total > 0:
    porcentaje_yuly = (gastado_yuly / presupuesto_yuly_total) * 100
    restante_yuly = presupuesto_yuly_total - gastado_yuly
    st.caption(f"📊 Yuly: {porcentaje_yuly:.1f}% usado - Restante: S/.{restante_yuly:.2f}")

st.markdown("---")

# ========== TABLA DE ÚLTIMOS MOVIMIENTOS ==========
st.markdown("### 📝 Últimos movimientos")

if not df_raw.empty:
    cols_disponibles = df_raw.columns.tolist()
    
    col_fecha = None
    col_responsable = None
    col_monto = None
    col_fondo = None
    
    for col in cols_disponibles:
        col_lower = col.lower()
        if 'fecha' in col_lower:
            col_fecha = col
        elif 'responsable' in col_lower or 'persona' in col_lower:
            col_responsable = col
        elif 'monto' in col_lower or 'soles' in col_lower:
            col_monto = col
        elif 'fondo' in col_lower or 'origen' in col_lower:
            col_fondo = col
    
    columnas_mostrar = [c for c in [col_fecha, col_responsable, col_monto, col_fondo] if c]
    
    if columnas_mostrar:
        df_ultimos = df_raw[columnas_mostrar].copy()
        nombres = ['📅 Fecha', '👤 Responsable', '💵 Monto', '🏦 Fondo']
        df_ultimos.columns = nombres[:len(columnas_mostrar)]
        st.dataframe(df_ultimos.tail(10), use_container_width=True)
    else:
        st.info("No se pudieron identificar las columnas. Columnas disponibles:")
        st.write(cols_disponibles)
else:
    st.info("No hay movimientos registrados aún")

st.markdown("---")
st.caption("🔄 Datos actualizados cada 60 segundos | 📱 Registra gastos en el formulario ParDuo")
