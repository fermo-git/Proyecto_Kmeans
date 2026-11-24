# Contenido para el documento PDF

> Copia este texto a Word/Google Docs, agrega las gráficas de la carpeta `graficas/` y las capturas del dashboard donde se indica, y exporta a PDF.

---

## 1. Portada

- **Nombre del proyecto:** Segmentación de clientes de un centro comercial mediante K-Means y desarrollo de un dashboard interactivo
- **Integrantes:** _(escribir nombres)_
- **Grupo:** _(escribir grupo)_
- **Fecha:** _(escribir fecha)_

---

## 2. Introducción y planteamiento del problema

**Temática:** análisis de clientes en el sector comercial.

**Problemática:** los centros comerciales tratan a todos sus clientes de la misma forma: las promociones, descuentos y campañas se dirigen a todo el público sin tomar en cuenta que cada cliente tiene un nivel de ingreso, un hábito de gasto y una frecuencia de visitas diferente. Esto provoca que muchas campañas no funcionen y que se desperdicien recursos de marketing.

**Justificación:** identificar grupos de clientes con características similares permite diseñar estrategias específicas para cada uno, mejorar la experiencia del cliente, aumentar las ventas y usar mejor el presupuesto de marketing. K-Means es adecuado porque no necesita datos etiquetados y encuentra los grupos de forma automática.

**Patrones que se buscan:** se espera encontrar grupos que combinen el nivel de ingreso con el nivel de gasto, por ejemplo clientes que ganan mucho y gastan mucho, clientes que ganan mucho pero gastan poco, clientes con poco ingreso que gastan mucho, etc.

---

## 3. Objetivos

**Objetivo general:** segmentar a los clientes de un centro comercial mediante el algoritmo K-Means para identificar grupos con comportamientos de compra similares y presentar los resultados en un dashboard interactivo.

**Objetivos específicos:**
1. Explorar, limpiar y preparar el dataset de clientes para su análisis.
2. Determinar el número óptimo de clústeres mediante el método del codo y el coeficiente de silueta.
3. Interpretar las características de cada clúster y asignarle un nombre descriptivo.
4. Desarrollar un dashboard interactivo que permita explorar los grupos y proponer recomendaciones de negocio.

---

## 4. Descripción del dataset

- **Fuente:** dataset propio, generado con Python (`codigo/generar_dataset.py`) simulando los registros de clientes de un centro comercial.
- **Registros:** 612 (594 después de la limpieza).
- **Variables:** 8

| Variable | Tipo | Descripción |
|---|---|---|
| ID_Cliente | Entero | Identificador del cliente |
| Genero | Texto | Femenino / Masculino |
| Edad | Entero | Edad en años |
| Ingreso_Anual | Decimal | Ingreso anual en miles de pesos |
| Puntaje_Gasto | Entero | Puntaje de 1 a 100 asignado según su gasto |
| Visitas_Mensuales | Entero | Número de visitas al mes |
| Gasto_Promedio | Decimal | Gasto promedio por visita en pesos |
| Membresia | Texto | Si / No tiene tarjeta de membresía |

**Variables elegidas para el agrupamiento:** Ingreso_Anual, Puntaje_Gasto y Visitas_Mensuales. Se eligieron porque describen directamente la capacidad económica del cliente, cuánto gasta y con qué frecuencia visita, que es lo que interesa para diseñar estrategias de marketing.

_(Insertar gráficas 01, 02, 03 y 04)_

---

## 5. Desarrollo del proyecto

**Exploración:** se revisaron los primeros 10 registros, dimensiones, tipos de datos, estadísticas descriptivas, nulos (14 en Edad, 10 en Ingreso_Anual y 8 en Genero) y 12 registros duplicados.

**Limpieza y preparación:**
- **Inconsistencias:** la columna Genero tenía valores como "M", "F", "MUJER", "Hombre" o con espacios; se unificaron a "Femenino" y "Masculino".
- **Tipos de datos:** Ingreso_Anual se leía como texto porque algunos valores tenían el signo "$"; se eliminó el símbolo y se convirtió a número. Edad se convirtió a entero.
- **Duplicados:** se eliminaron 12 registros duplicados.
- **Nulos:** Edad e Ingreso_Anual se rellenaron con la mediana (no se ve afectada por los atípicos) y Genero con la moda.
- **Atípicos:** se eliminaron 3 edades imposibles (3, 120 y 150 años) y 3 ingresos fuera del rango del método IQR (870, 950 y 1200 mil), ya que son errores de captura que afectarían los centroides. _(Insertar gráfica 05)_
- **Codificación:** Genero y Membresia se convirtieron a 0 y 1.
- **Escalamiento:** se aplicó StandardScaler a las tres variables del modelo, porque K-Means usa distancias y sin escalar el ingreso dominaría sobre las visitas.

**Implementación de K-Means:** se evaluaron los valores K = 2 a 8 usando la inercia (método del codo) y el coeficiente de silueta.

| K | Inercia | Silueta |
|---|---|---|
| 2 | 893.64 | 0.441 |
| 3 | 601.44 | 0.428 |
| 4 | 357.72 | 0.515 |
| **5** | **177.46** | **0.608** |
| 6 | 159.96 | 0.524 |
| 7 | 146.71 | 0.459 |
| 8 | 134.45 | 0.416 |

Se eligió **K = 5**: tiene la silueta más alta y es donde se forma el codo. _(Insertar gráfica 06)_

**Comparación de configuraciones (K = 3 vs K = 5):** con K = 3 la silueta es 0.43 y un grupo concentra 285 clientes, mezclando clientes con ingresos muy distintos. Con K = 5 la silueta sube a 0.61, la inercia baja de 601 a 177 y cada combinación de ingreso y gasto queda separada. _(Insertar gráfica 08)_

---

## 6. Resultados y análisis

**Centroides (valores originales):**

| Clúster | Segmento | Ingreso anual | Puntaje gasto | Visitas | Clientes |
|---|---|---|---|---|---|
| 0 | Promedio | 54.26 | 49.81 | 5.65 | 159 |
| 1 | Premium | 90.54 | 81.46 | 11.35 | 119 |
| 2 | Impulsivos | 26.26 | 77.88 | 9.44 | 97 |
| 3 | Ahorradores | 88.34 | 18.64 | 2.50 | 109 |
| 4 | Cautelosos | 26.76 | 18.84 | 2.76 | 110 |

**Tabla comparativa:**

| Segmento | Edad | Ingreso | Puntaje gasto | Visitas | Gasto promedio | % Membresía |
|---|---|---|---|---|---|---|
| Premium | 32.3 | 90.5 | 81.5 | 11.4 | 1668.12 | 76% |
| Ahorradores | 43.9 | 88.3 | 18.6 | 2.5 | 713.89 | 28% |
| Impulsivos | 24.3 | 26.3 | 77.9 | 9.4 | 1300.10 | 78% |
| Cautelosos | 49.0 | 26.8 | 18.8 | 2.8 | 420.40 | 25% |
| Promedio | 39.5 | 54.3 | 49.8 | 5.7 | 1018.71 | 33% |

_(Insertar gráficas 07, 09 y 10)_

**Interpretación de los grupos:**
- **Premium:** ingresos y gasto altos, visitan muy seguido y la mayoría tiene membresía. Son los clientes más valiosos.
- **Ahorradores:** ingresos altos pero gasto bajo y pocas visitas. Tienen capacidad de compra que no se está aprovechando.
- **Impulsivos:** los más jóvenes; tienen ingresos bajos pero gastan mucho y visitan seguido.
- **Cautelosos:** los de mayor edad, con ingresos y gasto bajos.
- **Promedio:** el grupo más grande, con valores medios en todo.

**Diferencias y similitudes:** Premium y Ahorradores tienen un ingreso casi igual pero un gasto opuesto; lo mismo pasa entre Impulsivos y Cautelosos. Premium e Impulsivos se parecen en gasto, visitas y membresía aunque su ingreso es muy distinto.

---

## 7. Dashboard

_(Insertar capturas de pantalla de ambas páginas del dashboard)_

El dashboard se desarrolló en Streamlit y tiene dos páginas:

- **Análisis general:** 4 KPI (total de clientes, ingreso promedio, puntaje de gasto promedio y visitas promedio), histogramas de edad e ingreso, clientes por género, relación visitas–gasto, estadísticas descriptivas y tabla de datos.
- **Segmentación K-Means:** clientes por clúster, gráfica de dispersión de los grupos, comparación de ingreso y gasto por segmento, visitas por segmento, tabla de estadísticas por clúster, método del codo y silueta, descripción de los grupos, hallazgos y recomendaciones.

**Filtros interactivos:** género, rango de edad, segmento y membresía. Todos los KPI, gráficas y tablas se actualizan con los filtros.

---

## 8. Conclusiones y recomendaciones

**Hallazgos:**
1. El ingreso no determina el gasto: los Ahorradores ganan casi lo mismo que los Premium, pero su puntaje de gasto es cuatro veces menor.
2. La frecuencia de visitas está muy relacionada con el gasto: los grupos que más visitan son los que más gastan.
3. Los Impulsivos son el grupo más joven y gastan mucho a pesar de tener ingresos bajos.

**Recomendaciones:**
1. Crear un programa de recompensas exclusivo para los clientes Premium para mantener su lealtad.
2. Diseñar promociones de productos de mayor valor y experiencias exclusivas para atraer a los Ahorradores.
3. Ofrecer descuentos, planes de pago y promociones de bajo costo para Impulsivos y Cautelosos.

**Limitaciones:**
- El modelo solo usa tres variables; no considera el tipo de productos comprados ni la temporada.
- K-Means supone grupos de forma circular y tamaño parecido, y es sensible a los valores atípicos.
- El dataset es simulado, por lo que los resultados deben validarse con datos reales.
