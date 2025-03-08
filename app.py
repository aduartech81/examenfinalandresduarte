import os
import sys
import subprocess

# Verificar si el entorno virtual ya está creado, si no, lo crea
VENV_PATH = "./venv"
if not os.path.exists(VENV_PATH):
    subprocess.run([sys.executable, "-m", "venv", VENV_PATH])

# Activar el entorno virtual y asegurarse de que las librerías están instaladas
pip_path = os.path.join(VENV_PATH, "bin", "pip") if sys.platform != "win32" else os.path.join(VENV_PATH, "Scripts", "pip")
subprocess.run([pip_path, "install", "--upgrade", "pip"])
subprocess.run([pip_path, "install", "plotly", "pandas", "streamlit", "matplotlib"])

# Importar las librerías después de instalarlas
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv("university_student_dashboard_data.csv")
    df["Year"] = df["Year"].astype(str)
    return df

df = load_data()

st.title("📊 Dashboard de Admisiones y Satisfacción Estudiantil")

st.sidebar.header("Filtros")
selected_year = st.sidebar.selectbox("Selecciona un Año", df["Year"].unique())

df_filtered = df[df["Year"] == selected_year]

st.header(f"📈 Resumen del Año {selected_year}")
col1, col2, col3 = st.columns(3)
col1.metric("Total Aplicaciones", df_filtered["Applications"].sum())
col2.metric("Total Admitidos", df_filtered["Admitted"].sum())
col3.metric("Total Matriculados", df_filtered["Enrolled"].sum())

st.header("📊 Tendencia de Retención y Satisfacción")
fig1 = px.line(df, x="Year", y=["Retention Rate (%)", "Student Satisfaction (%)"], title="Evolución de Retención y Satisfacción")
st.plotly_chart(fig1)

st.header("📊 Comparación entre Spring y Fall")
df_term = df.groupby("Term").sum()[["Applications", "Admitted", "Enrolled"]].reset_index()
fig2 = px.bar(df_term, x="Term", y=["Applications", "Admitted", "Enrolled"], title="Comparación de Aplicaciones, Admitidos y Matriculados", barmode="group")
st.plotly_chart(fig2)

st.header("📊 Distribución de Inscripción por Departamento")
dept_data = df[["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]].sum()
fig3 = px.pie(names=dept_data.index, values=dept_data.values, title="Distribución por Departamento")
st.plotly_chart(fig3)

st.success("✅ ¡Dashboard cargado exitosamente!")
