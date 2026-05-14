import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ========== CONFIGURACIÓN ==========
SHEET_ID = "1HRQo2fQyfJjB9RxIai9-1YfJQEFEXGW--Z2CrOdUPT0"

# URLs para las dos hojas
URL_RAW = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=1_Formulario_RAW"
URL_DASH = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=3_Dashboard_Data"

st.set_page_config(page_title="ParDuo", page_icon="😎", layout="wide")

@st.cache_data(ttl=60)
def cargar_formulario():
    """Carga la hoja 1_Formulario_RAW"""
    try:
        df = pd.read_csv(URL_RAW)
        return df
    except Exception as e:
        st.error(f"Error cargando formulario: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=60)
def cargar_dashboard():
    """Carga la hoja 3_Dashboard_Data"""
    try:
        df = pd.read_csv(URL_DASH)
        return df
    except Exception as e:
        st.error(f"Error cargando dashboard: {e}")
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
df_raw = cargar_formulario()
df_dash = cargar_dashboard()

# Verificar datos
if df_raw.empty:
    st.warning("⚠️ Cargando datos del formulario...")
if df_dash.empty:
    st.warning("⚠️ Cargando datos del dashboard...")

if df_raw.empty and df_dash.empty:
    st.stop()

# ========== CONVERTIR DASHBOARD A DICCIONARIO ==========
datos = {}
if not df_dash.empty and len(df_dash.columns) >= 2:
    for _, row in df_dash.iterrows():
        clave = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
        valor = row.iloc[1] if pd.notna(row.iloc[1]) else 0
        if clave and clave != "nan":
            datos[clave] = valor

# ========== EXTRAER VALORES CON NOMBRES CLAROS ==========
dinero_acumulado = float(datos.get('Dinero Acumulado', 11000))
dinero_invertido = float(datos.get('Dinero invertido', 80000))
presupuesto_jackson_total = float(datos.get('Presupuesto personal – Jackson', 300))
presupuesto_yuly_total = float(datos.get('Presupuesto personal – Yuly', 300))
gastos_variables_total = float(datos.get('Gastos Variables – Jackson', 0))
gastos_fijos_total = float(datos.get('Gastos Fijos – Yuly', 2000))

# Extraer valores de la hoja (columna C específica)
# Para esto, necesitamos buscar por la posición exacta
if not df_dash.empty:
    # Buscar valores por posición (asumiendo estructura conocida)
    try:
        # C8 = 📂 Gasto personal Jackson (gastado)
        gastado_jackson = float(df_dash.iloc[7, 1]) if len(df_dash) > 7 else 152.50
        # C9 = 📂 Gasto personal Yuly (gastado)
        gastado_yuly = float(df_dash.iloc[8, 1]) if len(df_dash) > 8 else 39.00
        # C11 = 📂 Gastos Fijos Yuly (gastado)
        gastado_fijos = float(df_dash.iloc[10, 1]) if len(df_dash) > 10 else 0
        # C19 = Gastos Variables – Jackson
        gastado_variables = float(df_dash.iloc[18, 1]) if len(df_dash) > 18 else 0
    except:
        gastado_jackson = 152.50
        gastado_yuly = 39.00
        gastado_fijos = 0
        gastado_variables = 0
else:
    gastado_jackson = 152.50
    gastado_yuly = 39.00
    gastado_fijos = 0
    gastado_variables = 0

# Cálculos de saldos restantes
restante_jackson = presupuesto_jackson_total - gastado_jackson
restante_yuly = presupuesto_yuly_total - gastado_yuly
restante_variables = dinero_acumulado - gastado_variables
restante_fijos = gastos_fijos_total - gastado_fijos

# Porcentajes para las barras de progreso
porcentaje_jackson = min(100, (gastado_jackson / presupuesto_jackson_total) * 100) if presupuesto_jackson_total > 0 else 0
porcentaje_yuly = min(100, (gastado_yuly / presupuesto_yuly_total) * 100) if presupuesto_yuly_total > 0 else 0

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

# ========== PRESUPUESTOS PERSONALES CON PROGRESS BAR ==========
st.markdown("### 🎯 Presupuesto Personal (S/.300 c/u)")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Jackson**")
    st.markdown(f"<h3 style='margin:0'>S/.{gastado_jackson:,.2f} <span style='font-size:16px; color:gray'>/ S/.{presupuesto_jackson_total:,.2f}</span></h3>", unsafe_allow_html=True)
    
    # Progress Bar estilo KPI financiero
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

# ========== GASTOS VARIABLES Y FIJOS CON PROGRESS BAR ==========
st.markdown("### 🏠 Gastos del Hogar")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**📂 Gastos Variables Jackson**")
    st.markdown(f"<h3 style='margin:0'>S/.{gastado_variables:,.2f} <span style='font-size:16px; color:gray'>/ S/.{dinero_acumulado:,.2f}</span></h3>", unsafe_allow_html=True)
    
    porcentaje_variables = min(100, (gastado_variables / dinero_acumulado) * 100) if dinero_acumulado > 0 else 0
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
    st.markdown(f"<h3 style='margin:0'>S/.{gastado_fijos:,.2f} <span style='font-size:16px; color:gray'>/ S/.{gastos_fijos_total:,.2f}</span></h3>", unsafe_allow_html=True)
    
    porcentaje_fijos = min(100, (gastado_fijos / gastos_fijos_total) * 100) if gastos_fijos_total > 0 else 0
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
    # Buscar las columnas correctas
    cols_disponibles = df_raw.columns.tolist()
    
    col_fecha = None
    col_responsable = None
    col_monto = None
    col_fondo = None
    
    for col in cols_disponibles:
        if 'fecha' in col.lower() or 'Fecha' in col:
            col_fecha = col
        if 'responsable' in col.lower() or 'Persona' in col:
            col_responsable = col
        if 'monto' in col.lower() or 'Monto' in col or 'soles' in col.lower():
            col_monto = col
        if 'fondo' in col.lower() or 'origen' in col.lower() or 'Fondo' in col:
            col_fondo = col
    
    # Seleccionar las columnas a mostrar
    columnas_mostrar = []
    for col in [col_fecha, col_responsable, col_monto, col_fondo]:
        if col:
            columnas_mostrar.append(col)
    
    if columnas_mostrar:
        df_ultimos = df_raw[columnas_mostrar].copy()
        # Renombrar para mejor visualización
        df_ultimos.columns = ['📅 Fecha', '👤 Responsable', '💵 Monto', '🏦 Fondo'][:len(columnas_mostrar)]
        st.dataframe(df_ultimos.tail(10), use_container_width=True)
    else:
        st.info("No se pudieron identificar las columnas. Las columnas disponibles son:")
        st.write(cols_disponibles)
else:
    st.info("No hay movimientos registrados aún")

# ========== FOOTER ==========
st.markdown("---")
st.caption("🔄 Datos actualizados cada 60 segundos | 📱 Registra gastos en el formulario ParDuo")
