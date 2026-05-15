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
        
        # FILAS 5 (índices 4) - Columna C (índice 2)
        ingreso_total = limpiar_valor(df_dash.iloc[4, 2] if num_cols > 2 else 0)       # Fila 5

        # FILAS 8 a 12 (índices 7 a 11) - Columna C (índice 2)
        gasto_personal_jackson = limpiar_valor(df_dash.iloc[7, 2] if num_cols > 2 else 0)     # Fila 8
        gasto_personal_yuly = limpiar_valor(df_dash.iloc[8, 2] if num_cols > 2 else 0)        # Fila 9
        gastos_variables = limpiar_valor(df_dash.iloc[9, 2] if num_cols > 2 else 0)           # Fila 10
        gastos_fijos = limpiar_valor(df_dash.iloc[10, 2] if num_cols > 2 else 0)              # Fila 11
        gasto_total = limpiar_valor(df_dash.iloc[11, 2] if num_cols > 2 else 0)               # Fila 12
        
        # FILAS 15 a 20 (índices 14 a 19) - Columna C (índice 2)
        dinero_mutuo = limpiar_valor(df_dash.iloc[14, 2] if num_cols > 2 else 0)              # Fila 15
        dinero_invertido = limpiar_valor(df_dash.iloc[15, 2] if num_cols > 2 else 0)          # Fila 16
        presupuesto_mensual_jackson = limpiar_valor(df_dash.iloc[16, 2] if num_cols > 2 else 0)   # Fila 17
        presupuesto_mensual_yuly = limpiar_valor(df_dash.iloc[17, 2] if num_cols > 2 else 0)      # Fila 18
        presupuesto_gastos_variables = limpiar_valor(df_dash.iloc[18, 2] if num_cols > 2 else 0)   # Fila 19
        presupuesto_gastos_fijos = limpiar_valor(df_dash.iloc[19, 2] if num_cols > 2 else 0)       # Fila 20
        
        # FILAS 24 a 27 (índices 23 a 26) - Columna C (índice 2)
        saldo_mensual_jackson = limpiar_valor(df_dash.iloc[23, 2] if num_cols > 2 else 0)      # Fila 24
        saldo_mensual_yuly = limpiar_valor(df_dash.iloc[24, 2] if num_cols > 2 else 0)         # Fila 25
        saldo_variables = limpiar_valor(df_dash.iloc[25, 2] if num_cols > 2 else 0)            # Fila 26
        saldo_fijos = limpiar_valor(df_dash.iloc[26, 2] if num_cols > 2 else 0)                # Fila 27
        
        # FILA 29 (índice 28) - Columna C (índice 2)
        ahorro_mutuo = limpiar_valor(df_dash.iloc[28, 2] if num_cols > 2 else 0)               # Fila 29
        
    else:
        # Valores por defecto si no hay suficientes filas (menos de 29 filas)
        ingreso_total = gasto_personal_jackson = gasto_personal_yuly = gastos_variables = gastos_fijos = 0
        gasto_total = 0
        dinero_mutuo = 0
        dinero_invertido = 0
        presupuesto_mensual_jackson = 0
        presupuesto_mensual_yuly = 0
        presupuesto_gastos_variables = 0
        presupuesto_gastos_fijos = 0
        saldo_mensual_jackson = saldo_mensual_yuly = saldo_variables = saldo_fijos = 0
        ahorro_mutuo = 0

else:
    # Valores por defecto si no hay datos (df_dash vacío)
    ingreso_total = gasto_personal_jackson = gasto_personal_yuly = gastos_variables = gastos_fijos = 0
    gasto_total = 0
    dinero_mutuo = 0
    dinero_invertido = 0
    presupuesto_mensual_jackson = 0
    presupuesto_mensual_yuly = 0
    presupuesto_gastos_variables = 0
    presupuesto_gastos_fijos = 0
    saldo_mensual_jackson = saldo_mensual_yuly = saldo_variables = saldo_fijos = 0
    ahorro_mutuo = 0


# ========== DISEÑO DE CUADRÍCULA SIMÉTRICA ==========
# CSS personalizado para bordes y líneas
st.markdown("""
<style>
    .main-border {
        border: 2px solid #333333;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .vertical-line {
        border-left: 1px solid #cccccc;
        border-right: 1px solid #cccccc;
    }
    .horizontal-line {
        border-top: 1px solid #cccccc;
        margin: 10px 0;
    }
    .row-fixed {
        min-height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }
    .empty-col {
        min-height: 300px;
    }
</style>
""", unsafe_allow_html=True)

# Contenedor principal con borde exterior
with st.container():
    st.markdown('<div class="main-border">', unsafe_allow_html=True)
    
    # Primera fila de columnas (izquierda, centro, derecha)
    col_left, col_center, col_right = st.columns([1, 2, 1])
    
    # COLUMNA 1 (izquierda - 25%) - VACÍA
    with col_left:
        st.markdown('<div class="empty-col"></div>', unsafe_allow_html=True)
    
    # COLUMNA CENTRAL (50%) - Contiene tus métricas
    with col_center:
        # Fila 1
        st.markdown('<div class="row-fixed">', unsafe_allow_html=True)
        # Aquí puedes poner tus métricas principales
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("🤝 DINERO MUTUO", f"S/.{dinero_mutuo:,.2f}")
            st.metric("💰 DINERO INVERTIDO", f"S/.{dinero_invertido:,.2f}")
        with col_b:
            st.metric("📊 INGRESO TOTAL", f"S/.{ingreso_total:,.2f}")
            st.metric("📉 GASTO TOTAL", f"S/.{gasto_total:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Línea horizontal divisoria
        st.markdown('<div class="horizontal-line"></div>', unsafe_allow_html=True)
        
        # Fila 2
        st.markdown('<div class="row-fixed">', unsafe_allow_html=True)
        # Más métricas
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("👤 GASTO JACKSON", f"S/.{gasto_personal_jackson:,.2f}")
            st.metric("👤 GASTO YULY", f"S/.{gasto_personal_yuly:,.2f}")
        with col_b:
            st.metric("🛒 GASTOS VARIABLES", f"S/.{gastos_variables:,.2f}")
            st.metric("🏠 GASTOS FIJOS", f"S/.{gastos_fijos:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # COLUMNA 4 (derecha - 25%) - VACÍA
    with col_right:
        st.markdown('<div class="empty-col"></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# ========== MOSTRAR VALORES EXTRAÍDOS ==========
st.markdown("---")
st.subheader("💰 valores extraídos de google sheets")

# Primera fila de métricas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🤝 dinero mutuo", f"S/.{dinero_mutuo:,.2f}")
with col2:
    st.metric("💰 dinero invertido", f"S/.{dinero_invertido:,.2f}")
with col3:
    st.metric("📊 ingreso total", f"S/.{ingreso_total:,.2f}")
with col4:
    st.metric("📉 gasto total", f"S/.{gasto_total:,.2f}")

# Segunda fila - Gastos por categoría
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("👤 gasto personal jackson", f"S/.{gasto_personal_jackson:,.2f}")
with col2:
    st.metric("👤 gasto personal yuly", f"S/.{gasto_personal_yuly:,.2f}")
with col3:
    st.metric("🛒 gastos variables", f"S/.{gastos_variables:,.2f}")
with col4:
    st.metric("🏠 gastos fijos", f"S/.{gastos_fijos:,.2f}")

# Tercera fila - Saldos restantes
st.markdown("### 📊 saldos restantes")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("✅ saldo mensual jackson", f"S/.{saldo_mensual_jackson:,.2f}")
with col2:
    st.metric("✅ saldo mensual yuly", f"S/.{saldo_mensual_yuly:,.2f}")
with col3:
    st.metric("✅ saldo variables", f"S/.{saldo_variables:,.2f}")
with col4:
    st.metric("✅ saldo fijos", f"S/.{saldo_fijos:,.2f}")

# Cuarta fila - Presupuestos
st.markdown("### 🎯 presupuestos")
col1, col2 = st.columns(2)
with col1:
    st.metric("💳 presupuesto mensual jackson", f"S/.{presupuesto_mensual_jackson:,.2f}")
    st.metric("💳 presupuesto mensual yuly", f"S/.{presupuesto_mensual_yuly:,.2f}")
with col2:
    st.metric("💸 presupuesto gastos variables", f"S/.{presupuesto_gastos_variables:,.2f}")
    st.metric("💸 presupuesto gastos fijos", f"S/.{presupuesto_gastos_fijos:,.2f}")

# Quinta fila - Ahorro
st.markdown("### 🏦 ahorro")
col1, col2 = st.columns(2)
with col1:
    st.metric("📊 ahorro mutuo", f"S/.{ahorro_mutuo:,.2f}")

st.markdown("---")

# ========== PORCENTAJES ==========
if presupuesto_mensual_jackson > 0:
    porcentaje_jackson = (gasto_personal_jackson / presupuesto_mensual_jackson) * 100
    restante_jackson = presupuesto_mensual_jackson - gasto_personal_jackson
    st.caption(f"📊 jackson: {porcentaje_jackson:.1f}% usado - restante: s/.{restante_jackson:.2f}")

if presupuesto_mensual_yuly > 0:
    porcentaje_yuly = (gasto_personal_yuly / presupuesto_mensual_yuly) * 100
    restante_yuly = presupuesto_mensual_yuly - gasto_personal_yuly
    st.caption(f"📊 yuly: {porcentaje_yuly:.1f}% usado - restante: s/.{restante_yuly:.2f}")

st.markdown("---")

# ========== TABLA DE ÚLTIMOS MOVIMIENTOS ==========
st.markdown("### 📝 últimos movimientos")

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
        nombres = ['📅 fecha', '👤 responsable', '💵 monto', '🏦 fondo']
        df_ultimos.columns = nombres[:len(columnas_mostrar)]
        st.dataframe(df_ultimos.tail(10), use_container_width=True)
    else:
        st.info("no se pudieron identificar las columnas. columnas disponibles:")
        st.write(cols_disponibles)
else:
    st.info("no hay movimientos registrados aún")

st.markdown("---")
st.caption("🔄 datos actualizados cada 60 segundos | 📱 registra gastos en el formulario paraduo")
