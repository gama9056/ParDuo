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

def encontrar_columna(df, posibles_nombres):
    """Busca una columna por posibles nombres"""
    for nombre in posibles_nombres:
        for col in df.columns:
            if nombre.lower() in col.lower():
                return col
    return None

# ========== TÍTULO ==========
st.markdown("<h1 style='text-align:center;'>😎 ParDuo - Finanzas Jackson & Yuly</h1>", unsafe_allow_html=True)

# ========== CARGAR DATOS ==========
df = cargar_datos()

if df.empty:
    st.warning("⚠️ Aún no hay datos. Registra gastos en el formulario de Google.")
    
    # Mostrar instrucciones
    with st.expander("📋 ¿Cómo registrar el primer gasto?"):
        st.markdown("""
        1. Abre el formulario ParDuo
        2. Completa los datos
        3. Envía el formulario
        4. Espera 30 segundos y refresca esta página
        """)
    st.stop()

# ========== IDENTIFICAR COLUMNAS AUTOMÁTICAMENTE ==========
with st.expander("🔧 Diagnóstico - Columnas encontradas"):
    st.write("**Nombres reales de las columnas en tu Google Sheets:**")
    for i, col in enumerate(df.columns):
        st.write(f"{i+1}. '{col}'")
    st.write(f"**Total de registros:** {len(df)}")
    st.write("**Primeros 2 registros:**")
    st.dataframe(df.head(2))

# Mapear columnas según posibles nombres
col_fecha = encontrar_columna(df, ['fecha', 'Fecha', 'Fecha del movimiento'])
col_responsable = encontrar_columna(df, ['responsable', 'Persona', 'Persona responsable'])
col_tipo = encontrar_columna(df, ['tipo', 'Tipo', 'Tipo de movimiento', 'movimiento'])
col_monto = encontrar_columna(df, ['monto', 'Monto', 'Monto en soles', 'soles'])
col_fondo = encontrar_columna(df, ['fondo', 'Fondo', 'Fondo de origen', 'origen'])
col_jackson_personal = encontrar_columna(df, ['Jackson', 'Gasto personal Jackson'])
col_yuly_personal = encontrar_columna(df, ['Yuly', 'Gasto personal Yuly'])
col_variables = encontrar_columna(df, ['Variables', 'Gastos Variables'])
col_fijos = encontrar_columna(df, ['Fijos', 'Gastos Fijos'])

# Verificar que encontramos las columnas necesarias
if not col_tipo:
    st.error("❌ No se encontró la columna 'Tipo de movimiento'")
    st.stop()

# ========== SEPARAR INGRESOS Y GASTOS ==========
# Buscar valores de ingreso/gasto
valores_tipo = df[col_tipo].unique()
st.sidebar.write("Valores en 'Tipo de movimiento':", valores_tipo)

gasto_valor = None
ingreso_valor = None
for v in valores_tipo:
    v_str = str(v).lower()
    if 'gasto' in v_str:
        gasto_valor = v
    if 'ingreso' in v_str:
        ingreso_valor = v

if gasto_valor and ingreso_valor:
    df_gastos = df[df[col_tipo] == gasto_valor]
    df_ingresos = df[df[col_tipo] == ingreso_valor]
else:
    # Si no encuentra, asume que todos son gastos
    df_gastos = df
    df_ingresos = pd.DataFrame()

# Calcular totales
total_gastos = df_gastos[col_monto].sum() if col_monto and not df_gastos.empty else 0
total_ingresos = df_ingresos[col_monto].sum() if col_monto and not df_ingresos.empty else 0

# ========== CREAR COLUMNAS ==========
col1, col2, col3, col4 = st.columns([1, 1, 1, 1.2])

with col1:
    st.markdown("### 📊 Resumen General")
    st.metric("💰 Ingresos", f"S/.{total_ingresos:,.2f}")
    st.metric("💸 Gastos", f"S/.{total_gastos:,.2f}")
    st.metric("📈 Balance", f"S/.{total_ingresos - total_gastos:,.2f}")

with col2:
    st.markdown("### 🎯 Presupuesto Personal (S/.300)")
    
    # Identificar Jackson y Yuly en fondo de origen
    if col_fondo:
        gastos_jackson = df_gastos[df_gastos[col_fondo].astype(str).str.contains('Jackson', case=False, na=False)]
        gastos_yuly = df_gastos[df_gastos[col_fondo].astype(str).str.contains('Yuly', case=False, na=False)]
        
        total_jackson = gastos_jackson[col_monto].sum() if not gastos_jackson.empty else 0
        total_yuly = gastos_yuly[col_monto].sum() if not gastos_yuly.empty else 0
        
        st.metric("Jackson", f"S/.{total_jackson:.2f} / S/.300")
        st.metric("Yuly", f"S/.{total_yuly:.2f} / S/.300")
        
        if total_jackson > 300:
            st.warning(f"⚠️ Jackson excedió en S/.{total_jackson - 300:.2f}")
        if total_yuly > 300:
            st.warning(f"⚠️ Yuly excedió en S/.{total_yuly - 300:.2f}")

with col3:
    st.markdown("### 🏠 Gastos del Hogar")
    
    if col_fondo:
        gastos_variables = df_gastos[df_gastos[col_fondo].astype(str).str.contains('Variables', case=False, na=False)]
        gastos_fijos = df_gastos[df_gastos[col_fondo].astype(str).str.contains('Fijos', case=False, na=False)]
        
        total_variables = gastos_variables[col_monto].sum() if not gastos_variables.empty else 0
        total_fijos = gastos_fijos[col_monto].sum() if not gastos_fijos.empty else 0
        
        st.metric("🛒 Gastos Variables (Jackson)", f"S/.{total_variables:,.2f}")
        st.metric("🏠 Gastos Fijos (Yuly)", f"S/.{total_fijos:,.2f}")

with col4:
    st.markdown("### 📅 Calendario")
    hoy = datetime.now()
    
    # Función para crear calendario simplificada
    def simple_calendar(df_cal, mes, año):
        cal = calendar.monthcalendar(año, mes)
        nombre_mes = calendar.month_name[mes]
        
        gastos_dia = {}
        if col_fecha and col_monto and not df_cal.empty:
            for _, row in df_cal.iterrows():
                try:
                    fecha = pd.to_datetime(row[col_fecha])
                    if fecha.month == mes and fecha.year == año:
                        dia = fecha.day
                        gastos_dia[dia] = gastos_dia.get(dia, 0) + float(row[col_monto])
                except:
                    pass
        
        html = f'<div style="background:#1e3c72; border-radius:10px; padding:10px; color:white;"><h5 style="text-align:center;">{nombre_mes}</h5><table style="width:100%; text-align:center;">'
        for semana in cal:
            html += "<tr>"
            for dia in semana:
                if dia == 0:
                    html += "<td style='color:#666;'>-</td>"
                else:
                    estilo = "background:#FF4444; border-radius:50%;" if dia in gastos_dia else ""
                    html += f"<td style='padding:5px;{estilo}'>{dia}</td>"
            html += "</tr>"
        html += "</table></div>"
        return html
    
    st.markdown(simple_calendar(df_gastos, hoy.month, hoy.year), unsafe_allow_html=True)

# ========== TABLA DE ÚLTIMOS REGISTROS ==========
st.markdown("---")
st.markdown("### 📝 Últimos movimientos")

# Mostrar columnas principales
cols_mostrar = [col_fecha, col_responsable, col_monto, col_fondo]
cols_mostrar = [c for c in cols_mostrar if c]
if cols_mostrar:
    st.dataframe(df[cols_mostrar].tail(10), use_container_width=True)

st.markdown("---")
st.caption("🔄 Los datos se actualizan cada 60 segundos | 💡 Configuración automática")
