import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import seaborn as sns
import matplotlib.pyplot as plt

# 1. CONFIGURACIÓN DE PÁGINA PROFESIONAL
st.set_page_config(
    page_title="Monitor Agro 2025 - Gran Rosario",
    page_icon="🌾",
    layout="wide"
)

# Estilo de encabezado
st.title("🌾 Monitor de Inteligencia Agroindustrial: Análisis 2025 y Proyecciones 2026")
st.markdown("""
**Nodo Portuario Gran Rosario.** Herramienta interactiva para el análisis de eficiencia logística y arbitraje.
*Fuentes integradas: GEA (BCR), SAGyP y reportes de Agroentregas.*
""")

# --- BARRA LATERAL ---
st.sidebar.header("📊 Dimensiones de Análisis")
opcion = st.sidebar.radio("Seleccioná un módulo:", 
                         ["Logística 2025 (Heatmap)", 
                          "Arbitraje de Precios (Basis)", 
                          "Análisis de Correlación"])

# --- MODULO 1: LOGÍSTICA (Basado en datos de Agroentregas 2025) ---
if opcion == "Logística 2025 (Heatmap)":
    st.header("🚛 Proyección de Flujo Logístico 2025")
    st.info("Estimación de arribo diario de camiones por terminal basado en intención de siembra y rindes GEA.")
    
    # Datos extraídos de tu mapa proyectado 2025
    data_2025 = {
        'Terminal': ['ADM Arroyo Seco', 'LDC Lagos', 'Cargill Alvear', 'Terminal 6', 'Vicentín San Lorenzo'],
        'Lat': [-33.15, -33.11, -33.05, -32.80, -32.75],
        'Lon': [-60.50, -60.55, -60.58, -60.65, -60.70],
        'Proyección 2025 (Cam/Día)': [1017, 1101, 1317, 1796, 1556]
    }
    df_map = pd.DataFrame(data_2025)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        m = folium.Map(location=[-33.0, -60.6], zoom_start=10, tiles="CartoDB positron")
        for idx, row in df_map.iterrows():
            folium.CircleMarker(
                location=[row['Lat'], row['Lon']],
                radius=row['Proyección 2025 (Cam/Día)']/100,
                color='red',
                fill=True,
                fill_opacity=0.6,
                popup=f"<b>{row['Terminal']}</b><br>Proyección: {row['Proyección 2025 (Cam/Día)']} camiones/día"
            ).add_to(m)
        st_folium(m, width=800, height=500)
    
    with col2:
        st.write("**Top Terminales 2025**")
        st.dataframe(df_map[['Terminal', 'Proyección 2025 (Cam/Día)']].sort_values(by='Proyección 2025 (Cam/Día)', ascending=False))

# --- MODULO 2: BASIS (FOB vs Pizarra con proyección 2026) ---
elif opcion == "Arbitraje de Precios (Basis)":
    st.header("💰 Convergencia de Precios Soja: FOB vs Pizarra")
    st.write("Análisis del diferencial (Basis) proyectado hacia Feb 2026.")

    # Datos proyectados 2025/26 extraídos de tus gráficos
    data_basis = {
        'Mes': ['Ene-Mar 25', 'Abr-Jun 25', 'Jul-Sep 25', 'Oct-Dic 25', 'Feb 2026 (Hoy)'],
        'FOB_Exportacion': [412.5, 430.2, 425.1, 437.8, 439.1],
        'Pizarra_Local': [349.6, 364.5, 360.2, 370.9, 372.1]
    }
    df_b = pd.DataFrame(data_basis)
    df_b['Basis'] = df_b['FOB_Exportacion'] - df_b['Pizarra_Local']

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(df_b['Mes'], df_b['FOB_Exportacion'], label='FOB 2025 (Exportación)', marker='s', color='#1a5276', linewidth=2)
    ax1.plot(df_b['Mes'], df_b['Pizarra_Local'], label='Pizarra 2025 (Estimado)', marker='o', color='#1e8449', linestyle='--')
    ax1.fill_between(df_b['Mes'], df_b['Pizarra_Local'], df_b['FOB_Exportacion'], color='#fcf3cf', alpha=0.5, label='Basis (Diferencial)')
    
    plt.title("Evolución Proyectada de Precios (USD/Ton)", fontsize=12)
    plt.ylabel("USD / Ton")
    plt.legend()
    plt.grid(True, alpha=0.3)
    st.pyplot(fig)
    
    st.success(f"Diferencial promedio proyectado: {df_b['Basis'].mean():.2f} USD/Ton")

# --- MODULO 3: CORRELACIÓN (Clima y Rinde 2025) ---
elif opcion == "Análisis de Correlación":
    st.header("📉 Matriz de Correlación 2025: Clima, Rinde y Precio")
    st.write("Sensibilidad del mercado ante variables climáticas (Datos GEA + SAGyP).")
    
    # Valores extraídos de tu matriz de correlación 2025
    corr_data = {
        'Rinde_Soja_qq': [1.00, 0.93, -0.34],
        'Precipitacion_mm': [0.93, 1.00, -0.20],
        'Precio_Promedio_USD': [-0.34, -0.20, 1.00]
    }
    df_corr = pd.DataFrame(corr_data, index=['Rinde_Soja_qq', 'Precipitacion_mm', 'Precio_Promedio_USD'])
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df_corr, annot=True, cmap='RdYlGn', center=0, ax=ax)
    plt.title("Interdependencia de Variables Campaña 2025")
    st.pyplot(fig)
    
    st.info("""
    **Interpretación técnica:**
    * Fuerte correlación positiva (0.93) entre precipitaciones y rinde.
    * Correlación negativa con el precio, validando la teoría de oferta y demanda en años de cosecha récord.
    """)

# --- PIE DE PÁGINA ---
st.divider()
st.caption("Desarrollado por Federico Flores | Data Science & Business Intelligence | 2025-2026")