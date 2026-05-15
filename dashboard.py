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
    
    num_filas = len(df_dash)
    num_cols = len(df_dash.columns)
    
    # Verificar que haya suficientes filas
    if num_filas > 28:  # Necesitas al menos 29 filas (0 a 28)
        
        # FILAS 5 a 12 (índices 4 a 11) - Columna C (índice 2)
        ingreso_total = limpiar_valor(df_dash.iloc[4, 2] if num_cols > 2 else 0)       # Fila 5
        gastado_jackson = limpiar_valor(df_dash.iloc[7, 2] if num_cols > 2 else 0)     # Fila 8
        gastado_yuly = limpiar_valor(df_dash.iloc[8, 2] if num_cols > 2 else 0)        # Fila 9
        gastado_variables = limpiar_valor(df_dash.iloc[9, 2] if num_cols > 2 else 0)   # Fila 10
        gastado_fijos = limpiar_valor(df_dash.iloc[10, 2] if num_cols > 2 else 0)      # Fila 11
        gastos_total = limpiar_valor(df_dash.iloc[11, 2] if num_cols > 2 else 0)       # Fila 12
        
        # FILAS 15 a 20 (índices 14 a 19) - Columna C (índice 2)
        dinero_acumulado = limpiar_valor(df_dash.iloc[14, 2] if num_cols > 2 else 0)   # Fila 15
        dinero_invertido = limpiar_valor(df_dash.iloc[15, 2] if num_cols > 2 else 0)   # Fila 16
        presupuesto_jackson_total = limpiar_valor(df_dash.iloc[16, 2] if num_cols > 2 else 0)  # Fila 17
        presupuesto_yuly_total = limpiar_valor(df_dash.iloc[17, 2] if num_cols > 2 else 0)     # Fila 18
        gastos_variables_base = limpiar_valor(df_dash.iloc[18, 2] if num_cols > 2 else 0)      # Fila 19
        gastos_fijos_base = limpiar_valor(df_dash.iloc[19, 2] if num_cols > 2 else 0)          # Fila 20
        
        # FILAS 24 a 27 (índices 23 a 26) - Columna C (índice 2)
        saldo_jackson = limpiar_valor(df_dash.iloc[23, 2] if num_cols > 2 else 0)       # Fila 24
        saldo_yuly = limpiar_valor(df_dash.iloc[24, 2] if num_cols > 2 else 0)          # Fila 25
        saldo_variables = limpiar_valor(df_dash.iloc[25, 2] if num_cols > 2 else 0)     # Fila 26
        saldo_fijos = limpiar_valor(df_dash.iloc[26, 2] if num_cols > 2 else 0)         # Fila 27
        
        # FILA 29 (índice 28) - Columna C (índice 2)
        total_disponible = limpiar_valor(df_dash.iloc[28, 2] if num_cols > 2 else 0)    # Fila 29
        
    else:
        # Valores por defecto si no hay suficientes filas
        ingreso_total = gastado_jackson = gastado_yuly = gastado_variables = gastado_fijos = 0
        gastos_total = 0
        dinero_acumulado = 12000
        dinero_invertido = 80000
        presupuesto_jackson_total = presupuesto_yuly_total = 300
        gastos_variables_base = gastos_fijos_base = 0
        saldo_jackson = saldo_yuly = saldo_variables = saldo_fijos = 0
        total_disponible = 0

else:
    # Valores por defecto si no hay datos
    ingreso_total = gastado_jackson = gastado_yuly = gastado_variables = gastado_fijos = 0
    gastos_total = 0
    dinero_acumulado = 12000
    dinero_invertido = 80000
    presupuesto_jackson_total = presupuesto_yuly_total = 300
    gastos_variables_base = gastos_fijos_base = 0
    saldo_jackson = saldo_yuly = saldo_variables = saldo_fijos = 0
    total_disponible = 0

# ========== MOSTRAR VALORES EXTRAÍDOS ==========
st.markdown("---")
st.subheader("💰 Valores extraídos de Google Sheets")

# Primera fila de métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💰 Dinero Acumulado", f"S/.{dinero_acumulado:,.2f}")
with col2:
    st.metric("📈 Dinero Invertido", f"S/.{dinero_invertido:,.2f}")
with col3:
    st.metric("📊 Ingreso Total", f"S/.{ingreso_total:,.2f}")
with col4:
    st.metric("📉 Gastos Total", f"S/.{gastos_total:,.2f}")

# Segunda fila - Gastos por categoría
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("👤 Gastado Jackson", f"S/.{gastado_jackson:,.2f}")
with col2:
    st.metric("👤 Gastado Yuly", f"S/.{gastado_yuly:,.2f}")
with col3:
    st.metric("🛒 Gastos Variables", f"S/.{gastado_variables:,.2f}")
with col4:
    st.metric("🏠 Gastos Fijos", f"S/.{gastado_fijos:,.2f}")

# Tercera fila - Saldos restantes
st.markdown("### 📊 Saldos Restantes")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("✅ Saldo Jackson", f"S/.{saldo_jackson:,.2f}")
with col2:
    st.metric("✅ Saldo Yuly", f"S/.{saldo_yuly:,.2f}")
with col3:
    st.metric("✅ Saldo Variables", f"S/.{saldo_variables:,.2f}")
with col4:
    st.metric("✅ Saldo Fijos", f"S/.{saldo_fijos:,.2f}")

# Cuarta fila - Totales
st.markdown("### 🎯 Totales")
col1, col2 = st.columns(2)
with col1:
    st.metric("🎯 Presupuesto Jackson", f"S/.{presupuesto_jackson_total:,.2f}")
    st.metric("🎯 Presupuesto Yuly", f"S/.{presupuesto_yuly_total:,.2f}")
with col2:
    st.metric("🏦 Total Disponible", f"S/.{total_disponible:,.2f}")
    st.metric("📊 Base Gastos Fijos", f"S/.{gastos_fijos_base:,.2f}")

st.markdown("---")

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
