import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# Parte 2. Obtencion y exploracion del dataset

df = pd.read_csv("datos/clientes_centro_comercial.csv")

print("Primeros 10 registros:")
print(df.head(10))

print("\nDimensiones:", df.shape)

print("\nColumnas:")
print(list(df.columns))

print("\nTipos de datos:")
print(df.dtypes)

print("\nEstadisticas descriptivas:")
print(df.describe(include="all"))

print("\nValores nulos por columna:")
print(df.isnull().sum())

print("\nRegistros duplicados:", df.duplicated().sum())

plt.figure(figsize=(8, 5))
sns.histplot(df["Edad"], bins=30, color="steelblue")
plt.title("Distribucion de la edad de los clientes")
plt.xlabel("Edad")
plt.ylabel("Cantidad de clientes")
plt.savefig("graficas/01_histograma_edad.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.histplot(df["Puntaje_Gasto"], bins=20, color="seagreen")
plt.title("Distribucion del puntaje de gasto")
plt.xlabel("Puntaje de gasto (1-100)")
plt.ylabel("Cantidad de clientes")
plt.savefig("graficas/02_histograma_puntaje_gasto.png")
plt.close()

plt.figure(figsize=(9, 5))
sns.countplot(x=df["Genero"], color="orange")
plt.title("Valores registrados en la columna Genero (antes de limpiar)")
plt.xlabel("Genero")
plt.ylabel("Cantidad")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("graficas/03_genero_sin_limpiar.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.scatterplot(x=df["Visitas_Mensuales"], y=df["Puntaje_Gasto"])
plt.title("Visitas mensuales vs puntaje de gasto")
plt.xlabel("Visitas mensuales")
plt.ylabel("Puntaje de gasto")
plt.savefig("graficas/04_visitas_vs_gasto.png")
plt.close()

# Parte 3. Limpieza y preparacion de datos

df["Genero"] = df["Genero"].str.strip().str.capitalize()
df["Genero"] = df["Genero"].replace({"M": "Masculino", "F": "Femenino", "Hombre": "Masculino", "Mujer": "Femenino"})
print("\nGenero despues de corregir inconsistencias:")
print(df["Genero"].value_counts(dropna=False))

df["Ingreso_Anual"] = df["Ingreso_Anual"].str.replace("$", "", regex=False)
df["Ingreso_Anual"] = pd.to_numeric(df["Ingreso_Anual"])

registros_antes = len(df)
df = df.drop_duplicates()
print("\nDuplicados eliminados:", registros_antes - len(df))

df["Edad"] = df["Edad"].fillna(df["Edad"].median())
df["Ingreso_Anual"] = df["Ingreso_Anual"].fillna(df["Ingreso_Anual"].median())
df["Genero"] = df["Genero"].fillna(df["Genero"].mode()[0])
print("\nNulos despues del tratamiento:")
print(df.isnull().sum())

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
sns.boxplot(y=df["Edad"], color="steelblue")
plt.title("Edad (con atipicos)")
plt.subplot(1, 2, 2)
sns.boxplot(y=df["Ingreso_Anual"], color="seagreen")
plt.title("Ingreso anual (con atipicos)")
plt.tight_layout()
plt.savefig("graficas/05_boxplot_atipicos.png")
plt.close()

edades_invalidas = df[(df["Edad"] < 18) | (df["Edad"] > 90)]
print("\nEdades fuera del rango 18-90:")
print(edades_invalidas[["ID_Cliente", "Edad"]])
df = df[(df["Edad"] >= 18) & (df["Edad"] <= 90)]

q1 = df["Ingreso_Anual"].quantile(0.25)
q3 = df["Ingreso_Anual"].quantile(0.75)
iqr = q3 - q1
limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr
ingresos_atipicos = df[(df["Ingreso_Anual"] < limite_inferior) | (df["Ingreso_Anual"] > limite_superior)]
print("\nLimites de ingreso (IQR):", limite_inferior, "-", limite_superior)
print("Ingresos atipicos:")
print(ingresos_atipicos[["ID_Cliente", "Ingreso_Anual"]])
df = df[(df["Ingreso_Anual"] >= limite_inferior) & (df["Ingreso_Anual"] <= limite_superior)]

df["Edad"] = df["Edad"].astype(int)

df["Genero_Cod"] = df["Genero"].map({"Femenino": 0, "Masculino": 1})
df["Membresia_Cod"] = df["Membresia"].map({"No": 0, "Si": 1})

print("\nDataset despues de la limpieza:")
print("Dimensiones:", df.shape)
print(df.dtypes)
print(df.describe())

variables = ["Ingreso_Anual", "Puntaje_Gasto", "Visitas_Mensuales"]

escalador = StandardScaler()
X = escalador.fit_transform(df[variables])

print("\nPrimeros 5 registros escalados:")
print(pd.DataFrame(X, columns=variables).head())

# Parte 4. Implementacion del algoritmo K-Means

valores_k = [2, 3, 4, 5, 6, 7, 8]
inercias = []
siluetas = []

for k in valores_k:
    modelo = KMeans(n_clusters=k, random_state=42, n_init=10)
    etiquetas = modelo.fit_predict(X)
    inercias.append(modelo.inertia_)
    siluetas.append(silhouette_score(X, etiquetas))

resultados_k = pd.DataFrame({"K": valores_k, "Inercia": inercias, "Silueta": siluetas})
print("\nEvaluacion de valores de K:")
print(resultados_k)
resultados_k.to_csv("datos/resultados_k.csv", index=False)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(valores_k, inercias, marker="o")
plt.title("Metodo del codo")
plt.xlabel("Numero de clusters (K)")
plt.ylabel("Inercia")
plt.grid(True, alpha=0.3)
plt.subplot(1, 2, 2)
plt.plot(valores_k, siluetas, marker="o", color="green")
plt.title("Coeficiente de silueta")
plt.xlabel("Numero de clusters (K)")
plt.ylabel("Silueta")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("graficas/06_codo_y_silueta.png")
plt.close()

k_final = 5
print("\nK seleccionado:", k_final)
print("Es el valor con mayor coeficiente de silueta y donde el codo deja de bajar de forma marcada.")

modelo_final = KMeans(n_clusters=k_final, random_state=42, n_init=10)
df["Cluster"] = modelo_final.fit_predict(X)

centroides = escalador.inverse_transform(modelo_final.cluster_centers_)
centroides_df = pd.DataFrame(centroides, columns=variables).round(2)
print("\nCentroides (valores originales):")
print(centroides_df)

print("\nRegistros por cluster:")
print(df["Cluster"].value_counts().sort_index())

print("\nInercia final:", modelo_final.inertia_)
print("Silueta final:", silhouette_score(X, df["Cluster"]))
print("Iteraciones:", modelo_final.n_iter_)

plt.figure(figsize=(9, 6))
plt.scatter(df["Ingreso_Anual"], df["Puntaje_Gasto"], c=df["Cluster"], cmap="viridis", s=40)
plt.scatter(centroides_df["Ingreso_Anual"], centroides_df["Puntaje_Gasto"], c="red", s=250, marker="X", label="Centroides")
plt.title("Agrupamiento de clientes (K = 5)")
plt.xlabel("Ingreso anual (miles)")
plt.ylabel("Puntaje de gasto")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig("graficas/07_clusters_k5.png")
plt.close()

modelo_3 = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster_K3"] = modelo_3.fit_predict(X)

print("\nComparacion de configuraciones:")
print("K = 3 -> Inercia:", round(modelo_3.inertia_, 2), " Silueta:", round(silhouette_score(X, df["Cluster_K3"]), 4))
print("K = 5 -> Inercia:", round(modelo_final.inertia_, 2), " Silueta:", round(silhouette_score(X, df["Cluster"]), 4))
print("\nRegistros por cluster con K = 3:")
print(df["Cluster_K3"].value_counts().sort_index())
print("\nCon K = 3 se juntan grupos con ingresos distintos pero gasto parecido,")
print("con K = 5 cada combinacion de ingreso y gasto queda en su propio grupo.")

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.scatter(df["Ingreso_Anual"], df["Puntaje_Gasto"], c=df["Cluster_K3"], cmap="viridis", s=30)
plt.title("Configuracion K = 3")
plt.xlabel("Ingreso anual (miles)")
plt.ylabel("Puntaje de gasto")
plt.subplot(1, 2, 2)
plt.scatter(df["Ingreso_Anual"], df["Puntaje_Gasto"], c=df["Cluster"], cmap="viridis", s=30)
plt.title("Configuracion K = 5")
plt.xlabel("Ingreso anual (miles)")
plt.ylabel("Puntaje de gasto")
plt.tight_layout()
plt.savefig("graficas/08_comparacion_k3_k5.png")
plt.close()

# Parte 5. Analisis e interpretacion de resultados

media_ingreso = df["Ingreso_Anual"].mean()
media_gasto = df["Puntaje_Gasto"].mean()

nombres = {}
for i in range(k_final):
    ingreso = centroides_df["Ingreso_Anual"][i]
    gasto = centroides_df["Puntaje_Gasto"][i]
    if ingreso > media_ingreso * 1.2 and gasto > media_gasto * 1.2:
        nombres[i] = "Premium"
    elif ingreso > media_ingreso * 1.2 and gasto < media_gasto * 0.8:
        nombres[i] = "Ahorradores"
    elif ingreso < media_ingreso * 0.8 and gasto > media_gasto * 1.2:
        nombres[i] = "Impulsivos"
    elif ingreso < media_ingreso * 0.8 and gasto < media_gasto * 0.8:
        nombres[i] = "Cautelosos"
    else:
        nombres[i] = "Promedio"

print("\nNombre asignado a cada cluster:")
print(nombres)

df["Segmento"] = df["Cluster"].map(nombres)

columnas_analisis = ["Edad", "Ingreso_Anual", "Puntaje_Gasto", "Visitas_Mensuales", "Gasto_Promedio"]

print("\nEstadisticas descriptivas por segmento:")
print(df.groupby("Segmento")[columnas_analisis].describe().round(2))

tabla_comparativa = df.groupby("Segmento")[columnas_analisis + ["Membresia_Cod"]].mean().round(2)
tabla_comparativa["Clientes"] = df["Segmento"].value_counts()
tabla_comparativa = tabla_comparativa.rename(columns={"Membresia_Cod": "Porcentaje_Membresia"})
tabla_comparativa["Porcentaje_Membresia"] = tabla_comparativa["Porcentaje_Membresia"] * 100
print("\nTabla comparativa de segmentos:")
print(tabla_comparativa)
tabla_comparativa.to_csv("datos/tabla_comparativa.csv")

plt.figure(figsize=(9, 5))
sns.barplot(x=tabla_comparativa.index, y=tabla_comparativa["Ingreso_Anual"], color="steelblue")
plt.title("Ingreso anual promedio por segmento")
plt.xlabel("Segmento")
plt.ylabel("Ingreso anual (miles)")
plt.savefig("graficas/09_ingreso_por_segmento.png")
plt.close()

plt.figure(figsize=(9, 5))
sns.boxplot(x=df["Segmento"], y=df["Edad"], color="orange")
plt.title("Edad por segmento")
plt.xlabel("Segmento")
plt.ylabel("Edad")
plt.savefig("graficas/10_edad_por_segmento.png")
plt.close()

df = df.drop(columns=["Cluster_K3"])
df.to_csv("datos/clientes_procesado.csv", index=False)
print("\nDataset procesado guardado en datos/clientes_procesado.csv")
print("Graficas guardadas en la carpeta graficas")
