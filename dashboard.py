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

# ========== EXTRAER VALORES DE LA HOJA 3_Dashboard_Data ==========
if not df_dash.empty:
    num_filas = len(df_dash)
    
    # Extraer por nombre (buscando en columna B, valor en columna C)
    datos_dict = {}
    for idx, row in df_dash.iterrows():
        # Tu texto está en columna 1 (B), el valor en columna 2 (C)
        nombre = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""  # ← Cambiado a columna 1
        valor_str = str(row.iloc[2]) if len(row) > 2 and pd.notna(row.iloc[2]) else "0"  # ← Cambiado a columna 2
        
        # Limpiar el valor: quitar "S/." y comas, convertir a número
        try:
            valor_limpio = valor_str.replace("S/.", "").replace(",", "").strip()
            valor = float(valor_limpio) if valor_limpio else 0
        except:
            valor = 0
            
        if nombre and nombre != "nan" and nombre != "":
            datos_dict[nombre] = valor
    
    # Extraer valores específicos por nombre (más confiable que por posición)
    gastado_jackson = datos_dict.get('📂 Gasto personal Jackson', 0)
    gastado_yuly = datos_dict.get('📂 Gasto personal Yuly', 0)
    gastado_variables = datos_dict.get('📂 Gastos Variables Jackson', 0)
    gastado_fijos = datos_dict.get('📂 Gastos Fijos Yuly', 0)
    
    dinero_acumulado = datos_dict.get('Dinero Acumulado', 11000)
    dinero_invertido = datos_dict.get('Dinero invertido', 80000)
    presupuesto_jackson_total = datos_dict.get('Presupuesto personal – Jackson', 300)
    presupuesto_yuly_total = datos_dict.get('Presupuesto personal – Yuly', 300)
    gastos_variables_base = datos_dict.get('Gastos Variables – Jackson', 0)
    gastos_fijos_base = datos_dict.get('Gastos Fijos – Yuly', 2000)
    
    # También extraer los valores de "Saldo restante" si los necesitas
    saldo_jackson = datos_dict.get('📂 Gasto personal Jackson', 0)  # Fila 24
    saldo_yuly = datos_dict.get('📂 Gasto personal Yuly', 0)        # Fila 25
    saldo_variables = datos_dict.get('📂 Gastos Variables Jackson', 0)  # Fila 26
    saldo_fijos = datos_dict.get('📂 Gastos Fijos Yuly', 0)         # Fila 27
    total_disponible = datos_dict.get('Total Disponible', 0)        # Fila 29

else:
    # Valores por defecto
    gastado_jackson = 152.50
    gastado_yuly = 39.00
    gastado_variables = 69.00
    gastado_fijos = 51.00
    dinero_acumulado = 12000
    dinero_invertido = 80000
    presupuesto_jackson_total = 300
    presupuesto_yuly_total = 300
    gastos_variables_base = 69.00
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

