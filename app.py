import streamlit as st
import pandas as pd
import plotly.express as px

# Carga de datos con caching para optimizar rendimiento
@st.cache_data
def load_data():
    df = pd.read_csv("data/university_student_dashboard_data.csv")
    df["Year"] = df["Year"].astype(str)
    return df

df = load_data()

# Título principal del dashboard
st.title("📊 Dashboard de Admisiones y Satisfacción Estudiantil")

# Sidebar con filtros
st.sidebar.header("Filtros 🔍")
selected_year = st.sidebar.selectbox("Selecciona un Año", sorted(df["Year"].unique(), reverse=True))

# Filtrado de datos según el año seleccionado
df_filtered = df[df["Year"] == selected_year]

# Métricas clave
st.header(f"📈 Resumen del Año {selected_year}")
col1, col2, col3 = st.columns(3)
col1.metric("Total Aplicaciones", f"{df_filtered['Applications'].sum():,}")
col2.metric("Total Admitidos", f"{df_filtered['Admitted'].sum():,}")
col3.metric("Total Matriculados", f"{df_filtered['Enrolled'].sum():,}")

# Gráfica de tendencia histórica
st.header("📊 Tendencia de Retención y Satisfacción")
fig1 = px.line(
    df,
    x="Year",
    y=["Retention Rate (%)", "Student Satisfaction (%)"],
    title="Evolución de Retención y Satisfacción",
    labels={"value": "Porcentaje", "variable": "Indicador"}
)
st.plotly_chart(fig1, use_container_width=True)

# Comparación Spring vs Fall
st.header("📊 Comparación entre Spring y Fall")
df_term = df.groupby("Term", as_index=False)[["Applications", "Admitted", "Enrolled"]].sum()
fig2 = px.bar(
    df_term,
    x="Term",
    y=["Applications", "Admitted", "Enrolled"],
    title="Comparación de Aplicaciones, Admitidos y Matriculados por Período",
    barmode="group",
    labels={"value": "Cantidad", "variable": "Categoría"}
)
st.plotly_chart(fig2, use_container_width=True)

# Distribución por departamento
st.header("📊 Distribución de Inscripción por Departamento")
dept_data = df[["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]].sum()
fig3 = px.pie(
    names=dept_data.index.str.replace(" Enrolled", ""),
    values=dept_data.values,
    title="Distribución por Departamento"
)
st.plotly_chart(fig3, use_container_width=True)

# Mensaje final de éxito
st.success("✅ ¡Dashboard cargado exitosamente!")
