# Segmentación de clientes de un centro comercial con K-Means

Proyecto integrador de la materia **Extracción de conocimiento en bases de datos**. Se aplica el algoritmo de aprendizaje no supervisado **K-Means** para agrupar a los clientes de un centro comercial según su ingreso, su nivel de gasto y su frecuencia de visitas. Los resultados se presentan en un dashboard interactivo hecho con **Streamlit**.

## Herramientas utilizadas

- Python 3
- Pandas
- Scikit-learn
- Matplotlib
- Seaborn
- Streamlit

## Estructura del repositorio

```
proyecto_kmeans/
├── codigo/
│   ├── generar_dataset.py      # Genera el dataset original
│   └── proyecto.py             # Exploración, limpieza, K-Means y análisis
├── dashboard/
│   └── dashboard.py            # Dashboard interactivo en Streamlit
├── datos/
│   ├── clientes_centro_comercial.csv   # Dataset original
│   ├── clientes_procesado.csv          # Dataset con clústeres asignados
│   ├── resultados_k.csv                # Inercia y silueta para cada K
│   └── tabla_comparativa.csv           # Promedios por segmento
├── graficas/                   # Gráficas generadas por proyecto.py
├── documentacion/              # Documento PDF del proyecto
├── requirements.txt
└── README.md
```

## Dataset

Dataset propio de **612 registros y 8 variables** (ID_Cliente, Genero, Edad, Ingreso_Anual, Puntaje_Gasto, Visitas_Mensuales, Gasto_Promedio, Membresia). Contiene a propósito valores nulos, registros duplicados, inconsistencias de texto y valores atípicos para aplicar las técnicas de limpieza.

## Instrucciones de ejecución

Todos los comandos se ejecutan desde la carpeta `proyecto_kmeans`.

1. Instalar las dependencias:

```
pip install -r requirements.txt
```

2. (Opcional) Volver a generar el dataset original:

```
python codigo/generar_dataset.py
```

3. Ejecutar el análisis (genera el dataset procesado y las gráficas):

```
python codigo/proyecto.py
```

4. Abrir el dashboard:

```
streamlit run dashboard/dashboard.py
```

El dashboard se abre en el navegador en `http://localhost:8501`.

## Resultados

Se evaluaron valores de K del 2 al 8 y se eligió **K = 5** por tener el mayor coeficiente de silueta (0.61). Los segmentos encontrados son: **Premium, Ahorradores, Impulsivos, Cautelosos y Promedio**.
