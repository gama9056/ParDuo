import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ========== CONFIGURACIÓN PARA JALAR DATOS DE GOOGLE SHEETS → ID + HOJAS DE INTERES==========
SHEET_ID = "1HRQo2fQyfJjB9RxIai9-1YfJQEFEXGW--Z2CrOdUPT0"

URL_RAW = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=1_Formulario_RAW"
URL_DASH = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=3_Dashboard_Data"

st.set_page_config(page_title="ParDuo", page_icon="😎", layout="wide")

@st.cache_data(ttl=60)
def cargar_formulario():
    try:
        df = pd.read_csv(URL_RAW)
        return df
    except Exception as e:
        st.error(f"Error cargando formulario: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def cargar_dashboard():
    try:
        df = pd.read_csv(URL_DASH)
        return df
    except Exception as e:
        st.error(f"Error cargando dashboard: {e}")
        return pd.DataFrame()

# ========== TÍTULO ==========
st.markdown("""
    <h1 style="color: black; margin-top: -70px; text-align: center; font-size: 30px; 
    font-family: 'Segoe UI'; text-shadow: 3px 3px 5px rgba(0,0,0,0.8); letter-spacing: 1px">😎 ParDuo</h1>
""", unsafe_allow_html=True)

# ========== CARGAR DATOS ==========
df_raw = cargar_formulario()
df_dash = cargar_dashboard()

if df_raw.empty:
    st.warning("⚠️ Cargando datos del formulario...")
if df_dash.empty:
    st.warning("⚠️ Cargando datos del dashboard...")

# ========== EXTRAER VALORES DE 3_Dashboard_Data ==========
if not df_dash.empty:
    num_filas = len(df_dash)
    
    # Extraer por nombre de la primera columna
    datos_dict = {}
    for idx, row in df_dash.iterrows():
        nombre = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
        valor = row.iloc[1] if len(row) > 1 and pd.notna(row.iloc[1]) else 0
        if nombre and nombre != "nan":
            datos_dict[nombre] = valor
    
    # Extraer por posición
    try:
        gastado_jackson = float(df_dash.iloc[7, 1]) if num_filas > 7 else 0
        gastado_yuly = float(df_dash.iloc[8, 1]) if num_filas > 8 else 0
        gastado_fijos = float(df_dash.iloc[10, 1]) if num_filas > 10 else 0
        dinero_acumulado = float(df_dash.iloc[14, 1]) if num_filas > 14 else 11000
        dinero_invertido = float(df_dash.iloc[15, 1]) if num_filas > 15 else 80000
        presupuesto_jackson_total = float(df_dash.iloc[16, 1]) if num_filas > 16 else 300
        presupuesto_yuly_total = float(df_dash.iloc[17, 1]) if num_filas > 17 else 300
        gastos_variables_base = float(df_dash.iloc[18, 1]) if num_filas > 18 else 0
        gastos_fijos_base = float(df_dash.iloc[19, 1]) if num_filas > 19 else 2000
    except Exception as e:
        gastado_jackson = 152.50
        gastado_yuly = 39.00
        gastado_fijos = 0
        dinero_acumulado = 11000
        dinero_invertido = 80000
        presupuesto_jackson_total = 300
        presupuesto_yuly_total = 300
        gastos_variables_base = 0
        gastos_fijos_base = 2000
    
    gastado_variables = float(datos_dict.get('📂 Gastos Variables Jackson', 0))
    if gastado_variables == 0:
        gastado_variables = float(datos_dict.get('Gastos Variables – Jackson', 0))
    
    gastado_fijos_dict = float(datos_dict.get('📂 Gastos Fijos Yuly', 0))
    if gastado_fijos_dict > 0:
        gastado_fijos = gastado_fijos_dict
else:
    gastado_jackson = 152.50
    gastado_yuly = 39.00
    gastado_fijos = 0
    gastado_variables = 0
    dinero_acumulado = 11000
    dinero_invertido = 80000
    presupuesto_jackson_total = 300
    presupuesto_yuly_total = 300
    gastos_variables_base = 0
    gastos_fijos_base = 2000

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
