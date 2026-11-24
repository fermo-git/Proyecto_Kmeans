import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Segmentacion de clientes", layout="wide")

df = pd.read_csv("datos/clientes_procesado.csv")
resultados_k = pd.read_csv("datos/resultados_k.csv")

st.title("Segmentación de clientes de un centro comercial con K-Means")

st.sidebar.header("Navegación")
pagina = st.sidebar.radio("Página", ["Análisis general", "Segmentación K-Means"])

st.sidebar.header("Filtros")
lista_generos = list(df["Genero"].unique())
generos = st.sidebar.multiselect("Género", lista_generos, default=lista_generos)

edad_minima = int(df["Edad"].min())
edad_maxima = int(df["Edad"].max())
rango_edad = st.sidebar.slider("Rango de edad", edad_minima, edad_maxima, (edad_minima, edad_maxima))

lista_segmentos = list(df["Segmento"].unique())
segmentos = st.sidebar.multiselect("Segmento", lista_segmentos, default=lista_segmentos)

membresia = st.sidebar.selectbox("Membresía", ["Todos", "Si", "No"])

filtrado = df[df["Genero"].isin(generos)]
filtrado = filtrado[(filtrado["Edad"] >= rango_edad[0]) & (filtrado["Edad"] <= rango_edad[1])]
filtrado = filtrado[filtrado["Segmento"].isin(segmentos)]
if membresia != "Todos":
    filtrado = filtrado[filtrado["Membresia"] == membresia]

if len(filtrado) == 0:
    st.warning("No hay clientes con los filtros seleccionados.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de clientes", len(filtrado))
col2.metric("Ingreso anual promedio", str(round(filtrado["Ingreso_Anual"].mean(), 1)) + " mil")
col3.metric("Puntaje de gasto promedio", round(filtrado["Puntaje_Gasto"].mean(), 1))
col4.metric("Visitas mensuales promedio", round(filtrado["Visitas_Mensuales"].mean(), 1))

if pagina == "Análisis general":
    st.header("Análisis general del dataset")

    izquierda, derecha = st.columns(2)

    fig, ax = plt.subplots()
    sns.histplot(filtrado["Edad"], bins=20, color="steelblue", ax=ax)
    ax.set_title("Distribución de edad")
    izquierda.pyplot(fig)

    fig, ax = plt.subplots()
    sns.histplot(filtrado["Ingreso_Anual"], bins=20, color="seagreen", ax=ax)
    ax.set_title("Distribución del ingreso anual (miles)")
    derecha.pyplot(fig)

    izquierda, derecha = st.columns(2)

    fig, ax = plt.subplots()
    sns.countplot(x=filtrado["Genero"], color="orange", ax=ax)
    ax.set_title("Clientes por género")
    izquierda.pyplot(fig)

    fig, ax = plt.subplots()
    sns.scatterplot(x=filtrado["Visitas_Mensuales"], y=filtrado["Puntaje_Gasto"], ax=ax)
    ax.set_title("Visitas mensuales vs puntaje de gasto")
    derecha.pyplot(fig)

    st.subheader("Estadísticas descriptivas")
    st.dataframe(filtrado[["Edad", "Ingreso_Anual", "Puntaje_Gasto", "Visitas_Mensuales", "Gasto_Promedio"]].describe().round(2))

    st.subheader("Datos")
    st.dataframe(filtrado)

else:
    st.header("Segmentación mediante K-Means")

    izquierda, derecha = st.columns(2)

    fig, ax = plt.subplots()
    sns.countplot(x=filtrado["Segmento"], color="steelblue", ax=ax)
    ax.set_title("Clientes por clúster")
    izquierda.pyplot(fig)

    fig, ax = plt.subplots()
    sns.scatterplot(x=filtrado["Ingreso_Anual"], y=filtrado["Puntaje_Gasto"], hue=filtrado["Segmento"], palette="viridis", ax=ax)
    ax.set_title("Ingreso anual vs puntaje de gasto")
    ax.set_xlabel("Ingreso anual (miles)")
    ax.set_ylabel("Puntaje de gasto")
    derecha.pyplot(fig)

    izquierda, derecha = st.columns(2)

    promedios = filtrado.groupby("Segmento")[["Ingreso_Anual", "Puntaje_Gasto"]].mean()

    fig, ax = plt.subplots()
    promedios.plot(kind="bar", ax=ax)
    ax.set_title("Ingreso y puntaje de gasto promedio por segmento")
    ax.set_xlabel("Segmento")
    izquierda.pyplot(fig)

    fig, ax = plt.subplots()
    sns.boxplot(x=filtrado["Segmento"], y=filtrado["Visitas_Mensuales"], color="orange", ax=ax)
    ax.set_title("Visitas mensuales por segmento")
    derecha.pyplot(fig)

    st.subheader("Estadísticas descriptivas por clúster")
    tabla = filtrado.groupby("Segmento")[["Edad", "Ingreso_Anual", "Puntaje_Gasto", "Visitas_Mensuales", "Gasto_Promedio"]].mean().round(2)
    tabla["Clientes"] = filtrado["Segmento"].value_counts()
    st.dataframe(tabla)

    st.subheader("Resultados del modelo")
    izquierda, derecha = st.columns(2)

    fig, ax = plt.subplots()
    ax.plot(resultados_k["K"], resultados_k["Inercia"], marker="o")
    ax.set_title("Método del codo")
    ax.set_xlabel("K")
    ax.set_ylabel("Inercia")
    izquierda.pyplot(fig)

    fig, ax = plt.subplots()
    ax.plot(resultados_k["K"], resultados_k["Silueta"], marker="o", color="green")
    ax.set_title("Coeficiente de silueta")
    ax.set_xlabel("K")
    ax.set_ylabel("Silueta")
    derecha.pyplot(fig)

    st.write("Se eligió **K = 5** porque tiene el coeficiente de silueta más alto (0.61) y a partir de ese valor la inercia casi no disminuye.")

    st.subheader("Descripción de los grupos")
    st.markdown("""
- **Premium:** ingresos altos y gasto alto. Visitan el centro comercial muy seguido y la mayoría tiene membresía.
- **Ahorradores:** ingresos altos pero gastan poco. Visitan pocas veces al mes.
- **Impulsivos:** clientes jóvenes con ingresos bajos que gastan mucho y visitan con frecuencia.
- **Cautelosos:** ingresos bajos y gasto bajo, son los de mayor edad y los que menos compran.
- **Promedio:** ingresos y gasto medios. Es el grupo más grande.
""")

    st.subheader("Hallazgos y recomendaciones")
    st.markdown("""
**Hallazgos**
1. El ingreso no determina el gasto: los Ahorradores ganan casi lo mismo que los Premium pero su puntaje de gasto es cuatro veces menor.
2. Las visitas mensuales están muy relacionadas con el gasto: los grupos que más visitan (Premium e Impulsivos) son los que más gastan.
3. Los Impulsivos son el grupo más joven (24 años en promedio) y gastan mucho a pesar de tener ingresos bajos.

**Recomendaciones**
1. Crear un programa de recompensas exclusivo para los clientes Premium para mantener su lealtad.
2. Lanzar promociones de productos de mayor valor dirigidas a los Ahorradores para aumentar su gasto.
3. Ofrecer descuentos y planes de pago para los Impulsivos y campañas de bajo costo para los Cautelosos.

**Limitaciones:** el modelo solo usa tres variables, K-Means supone grupos de forma circular y es sensible a los valores atípicos, por lo que los resultados dependen de la limpieza realizada.
""")
