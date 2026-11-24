import numpy as np
import pandas as pd

np.random.seed(42)

grupos = [
    [120, 33, 90, 82, 12],
    [110, 45, 88, 18, 3],
    [100, 24, 25, 78, 10],
    [110, 50, 26, 20, 3],
    [160, 40, 55, 50, 6],
]

edades = []
ingresos = []
puntajes = []
visitas = []
membresias = []

for grupo in grupos:
    n = grupo[0]
    for i in range(n):
        edad = int(np.random.normal(grupo[1], 7))
        if edad < 18:
            edad = 18
        if edad > 70:
            edad = 70
        ingreso = round(np.random.normal(grupo[2], 8), 1)
        if ingreso < 10:
            ingreso = 10
        puntaje = int(np.random.normal(grupo[3], 7))
        if puntaje < 1:
            puntaje = 1
        if puntaje > 100:
            puntaje = 100
        visita = int(np.random.normal(grupo[4], 1.5))
        if visita < 1:
            visita = 1
        if puntaje > 60 and np.random.rand() < 0.7:
            membresia = "Si"
        elif np.random.rand() < 0.25:
            membresia = "Si"
        else:
            membresia = "No"
        edades.append(edad)
        ingresos.append(ingreso)
        puntajes.append(puntaje)
        visitas.append(visita)
        membresias.append(membresia)

df = pd.DataFrame({
    "Edad": edades,
    "Ingreso_Anual": ingresos,
    "Puntaje_Gasto": puntajes,
    "Visitas_Mensuales": visitas,
    "Membresia": membresias,
})

df["Gasto_Promedio"] = (df["Puntaje_Gasto"] * 15 + df["Ingreso_Anual"] * 5 + np.random.normal(0, 80, len(df))).round(2)
df["Genero"] = np.random.choice(["Femenino", "Masculino"], len(df))

df = df.sample(frac=1, random_state=42).reset_index(drop=True)
df.insert(0, "ID_Cliente", range(1, len(df) + 1))
df = df[["ID_Cliente", "Genero", "Edad", "Ingreso_Anual", "Puntaje_Gasto", "Visitas_Mensuales", "Gasto_Promedio", "Membresia"]]

df["Edad"] = df["Edad"].astype(object)
df["Ingreso_Anual"] = df["Ingreso_Anual"].astype(object)

variantes = ["M", "F", "masculino", "femenino ", " Masculino", "MUJER", "Hombre"]
for i in np.random.choice(len(df), 25, replace=False):
    df.loc[i, "Genero"] = np.random.choice(variantes)

for i in np.random.choice(len(df), 15, replace=False):
    df.loc[i, "Ingreso_Anual"] = "$" + str(df.loc[i, "Ingreso_Anual"])

for i in np.random.choice(len(df), 14, replace=False):
    df.loc[i, "Edad"] = np.nan
for i in np.random.choice(len(df), 10, replace=False):
    df.loc[i, "Ingreso_Anual"] = np.nan
for i in np.random.choice(len(df), 8, replace=False):
    df.loc[i, "Genero"] = np.nan

df.loc[5, "Edad"] = 150
df.loc[77, "Edad"] = 120
df.loc[210, "Edad"] = 3
df.loc[340, "Ingreso_Anual"] = 950.0
df.loc[455, "Ingreso_Anual"] = 870.0
df.loc[512, "Ingreso_Anual"] = 1200.0

duplicados = df.sample(12, random_state=1)
df = pd.concat([df, duplicados], ignore_index=True)

df.to_csv("datos/clientes_centro_comercial.csv", index=False)
print("Dataset generado:", df.shape)
