import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image

# ---------------------- Configuración de página ----------------------
st.set_page_config(page_title="Recomendador Café Quiteñito - Kappa", page_icon="☕", layout="wide")
st.title("☕ Recomendador de Platos - Arquitectura Kappa (Café Quiteñito)")

# ---------------------- Estilos personalizados ----------------------
with open("style/main.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------- Logo y encabezado ----------------------
logo = Image.open("Imagenes/logotecazuay.PNG")
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 Café Quiteñito")
    st.markdown("#### Implementación de Arquitectura Kappa por Karina Chisaguano")
with col2:
    st.image(logo, width=250)

# -----------------------------------------------------------
# CAPA ÚNICA DE STREAM - Flujo continuo de datos
# -----------------------------------------------------------
st.header("🌐 Capa Única de Procesamiento en Flujo (Stream)")

# Simulación de flujo histórico como evento continuo
platos = ["Capuccino", "Latte", "Mocaccino", "Cheesecake", "Croissant", "Sandwich de Jamón"]
usuarios = [f"Cliente_{i}" for i in range(1, 11)]

# Inicialización del flujo en la sesión
if "flujo_valoraciones" not in st.session_state:
    # Cargamos los datos históricos como si fueran los primeros eventos del flujo
    historico = pd.read_csv("historico_cafeteria_2025.csv")
    historico["fecha"] = pd.to_datetime(historico.get("fecha", datetime.now()))
    st.session_state["flujo_valoraciones"] = historico

# Formulario de entrada en tiempo real
st.subheader("🕐 Ingreso de nueva valoración (flujo en tiempo real)")
nuevo_usuario = st.text_input("👤 Nombre del cliente", "Cliente_nuevo")
plato_nuevo = st.selectbox("🍽️ Selecciona el plato", platos)
valor_nuevo = st.slider("⭐ Valoración del plato (1-5)", 1, 5, 4)

if st.button("Registrar valoración"):
    nuevo_evento = pd.DataFrame({
        "usuario": [nuevo_usuario],
        "plato": [plato_nuevo],
        "valoracion": [valor_nuevo],
        "fecha": [datetime.now()]
    })
    # Añadir el evento al flujo continuo
    st.session_state["flujo_valoraciones"] = pd.concat(
        [st.session_state["flujo_valoraciones"], nuevo_evento], ignore_index=True
    )
    st.success("✅ Nueva valoración añadida al flujo Kappa.")

# -----------------------------------------------------------
# PROCESAMIENTO CONTINUO DEL FLUJO
# -----------------------------------------------------------
st.header("⚙️ Procesamiento continuo de eventos")

# Simulamos un cálculo continuo de promedios en el flujo actual
flujo_actual = st.session_state["flujo_valoraciones"]
flujo_actual["valoracion"] = pd.to_numeric(flujo_actual["valoracion"], errors="coerce")

promedios = flujo_actual.groupby("plato")["valoracion"].mean().reset_index()
promedios = promedios.sort_values(by="valoracion", ascending=False)

# Mostrar resultados actualizados
st.subheader("🍰 Recomendaciones actualizadas en tiempo real")
st.table(promedios.style.format({"valoracion": "{:.2f}"}))

# Plato más recomendado del flujo actual
top_plato = promedios.iloc[0]["plato"]
st.success(f"🥇 Plato más recomendado en tiempo real: **{top_plato}**")

# Visualización dinámica
st.subheader("📊 Valoraciones promedio por plato (flujo continuo)")
st.bar_chart(promedios.set_index("plato"))

# -----------------------------------------------------------
# MONITOREO DEL FLUJO
# -----------------------------------------------------------
st.header("📡 Flujo completo de eventos registrados")
st.dataframe(flujo_actual.tail(10), use_container_width=True)
st.info("La arquitectura Kappa procesa tanto los datos históricos como los nuevos desde un único flujo de eventos.")
