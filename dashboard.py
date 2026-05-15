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
    # Limpiar valor: quita "S/." y comas, convierte a número
    def limpiar_valor(valor_str):
        try:
            return float(str(valor_str).replace("S/.", "").replace(",", "").strip())
        except:
            return 0
    
    # Extraer por posición (fila, columna) - columna C es índice 2
    gastado_jackson = limpiar_valor(df_dash.iloc[7, 2])   # Fila 8, Columna C
    gastado_yuly = limpiar_valor(df_dash.iloc[8, 2])      # Fila 9, Columna C
    gastado_variables = limpiar_valor(df_dash.iloc[9, 2]) # Fila 10, Columna C
    gastado_fijos = limpiar_valor(df_dash.iloc[10, 2])    # Fila 11, Columna C
    
    dinero_acumulado = limpiar_valor(df_dash.iloc[14, 2]) # Fila 15, Columna C
    dinero_invertido = limpiar_valor(df_dash.iloc[15, 2]) # Fila 16, Columna C
    presupuesto_jackson_total = limpiar_valor(df_dash.iloc[16, 2]) # Fila 17, Columna C
    presupuesto_yuly_total = limpiar_valor(df_dash.iloc[17, 2])    # Fila 18, Columna C
    gastos_variables_base = limpiar_valor(df_dash.iloc[18, 2])      # Fila 19, Columna C
    gastos_fijos_base = limpiar_valor(df_dash.iloc[19, 2])          # Fila 20, Columna C
    
    # También los saldos restantes (ya calculados en Sheets)
    saldo_jackson = limpiar_valor(df_dash.iloc[23, 2])   # Fila 24, Columna C
    saldo_yuly = limpiar_valor(df_dash.iloc[24, 2])      # Fila 25, Columna C
    saldo_variables = limpiar_valor(df_dash.iloc[25, 2]) # Fila 26, Columna C
    saldo_fijos = limpiar_valor(df_dash.iloc[26, 2])     # Fila 27, Columna C
    total_disponible = limpiar_valor(df_dash.iloc[28, 2]) # Fila 29, Columna C

else:
    # Valores por defecto
    gastado_jackson = 152.50
    gastado_yuly = 39.00
    gastado_variables = 69.00
    gastado_fijos = 51.00
    dinero_acumulado = 12000.00
    dinero_invertido = 80000.00
    presupuesto_jackson_total = 300.00
    presupuesto_yuly_total = 300.00
    gastos_variables_base = 69.00
    gastos_fijos_base = 2000.00

# ========== CÁLCULOS ==========
restante_jackson = presupuesto_jackson_total - gastado_jackson
restante_yuly = presupuesto_yuly_total - gastado_yuly
restante_variables = gastos_variables_base - gastado_variables if gastos_variables_base > 0 else dinero_acumulado - gastado_variables
restante_fijos = gastos_fijos_base - gastado_fijos

porcentaje_jackson = min(100, (gastado_jackson / presupuesto_jackson_total) * 100) if presupuesto_jackson_total > 0 else 0
porcentaje_yuly = min(100, (gastado_yuly / presupuesto_yuly_total) * 100) if presupuesto_yuly_total > 0 else 0
porcentaje_variables = min(100, (gastado_variables / gastos_variables_base) * 100) if gastos_variables_base > 0 else 0
porcentaje_fijos = min(100, (gastado_fijos / gastos_fijos_base) * 100) if gastos_fijos_base > 0 else 0

# ========== KPI CARDS ==========
st.markdown("### 📊 Resumen General")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Dinero Acumulado", f"S/.{dinero_acumulado:,.2f}")
with col2:
    st.metric("📈 Dinero Invertido", f"S/.{dinero_invertido:,.2f}")
with col3:
    st.metric("🛒 Gastos Variables", f"S/.{gastado_variables:,.2f}")
with col4:
    st.metric("🏠 Gastos Fijos", f"S/.{gastado_fijos:,.2f}")

st.markdown("---")

# ========== PRESUPUESTOS PERSONALES ==========
st.markdown("### 🎯 Presupuesto Personal (S/.300 c/u)")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Jackson**")
    st.markdown(f"<h3 style='margin:0'>S/.{gastado_jackson:,.2f} <span style='font-size:16px; color:gray'>/ S/.{presupuesto_jackson_total:,.2f}</span></h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background-color: #e0e0e0; border-radius: 10px; height: 25px; width: 100%; margin: 10px 0;">
        <div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); 
                    width: {porcentaje_jackson}%; 
                    border-radius: 10px; 
                    height: 25px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: flex-end;
                    padding-right: 8px;
                    color: white;
                    font-size: 12px;">
            {porcentaje_jackson:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"💰 Restante: S/.{restante_jackson:,.2f}")

with col2:
    st.markdown(f"**Yuly**")
    st.markdown(f"<h3 style='margin:0'>S/.{gastado_yuly:,.2f} <span style='font-size:16px; color:gray'>/ S/.{presupuesto_yuly_total:,.2f}</span></h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background-color: #e0e0e0; border-radius: 10px; height: 25px; width: 100%; margin: 10px 0;">
        <div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); 
                    width: {porcentaje_yuly}%; 
                    border-radius: 10px; 
                    height: 25px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: flex-end;
                    padding-right: 8px;
                    color: white;
                    font-size: 12px;">
            {porcentaje_yuly:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"💰 Restante: S/.{restante_yuly:,.2f}")

st.markdown("---")

# ========== GASTOS VARIABLES Y FIJOS ==========
st.markdown("### 🏠 Gastos del Hogar")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**📂 Gastos Variables Jackson**")
    base_text = f"/ S/.{gastos_variables_base:,.2f}" if gastos_variables_base > 0 else ""
    st.markdown(f"<h3 style='margin:0'>S/.{gastado_variables:,.2f} <span style='font-size:16px; color:gray'>{base_text}</span></h3>", unsafe_allow_html=True)
    
    if gastos_variables_base > 0:
        st.markdown(f"""
        <div style="background-color: #e0e0e0; border-radius: 10px; height: 25px; width: 100%; margin: 10px 0;">
            <div style="background: linear-gradient(90deg, #4ECDC4 0%, #44b3b0 100%); 
                        width: {porcentaje_variables}%; 
                        border-radius: 10px; 
                        height: 25px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: flex-end;
                        padding-right: 8px;
                        color: white;
                        font-size: 12px;">
                {porcentaje_variables:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.caption(f"💰 Restante: S/.{restante_variables:,.2f}")

with col2:
    st.markdown(f"**📂 Gastos Fijos Yuly**")
    st.markdown(f"<h3 style='margin:0'>S/.{gastado_fijos:,.2f} <span style='font-size:16px; color:gray'>/ S/.{gastos_fijos_base:,.2f}</span></h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background-color: #e0e0e0; border-radius: 10px; height: 25px; width: 100%; margin: 10px 0;">
        <div style="background: linear-gradient(90deg, #FF6B6B 0%, #e55555 100%); 
                    width: {porcentaje_fijos}%; 
                    border-radius: 10px; 
                    height: 25px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: flex-end;
                    padding-right: 8px;
                    color: white;
                    font-size: 12px;">
            {porcentaje_fijos:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption(f"💰 Restante: S/.{restante_fijos:,.2f}")

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

