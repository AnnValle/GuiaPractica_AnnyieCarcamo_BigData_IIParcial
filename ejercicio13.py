import pandas as pd
import numpy as np

df = pd.read_csv("ventas.csv")
df_limpio = df.dropna().drop_duplicates().copy()


df_limpio['Cliente'] = df_limpio['Cliente'].str.title()
df_limpio['Producto'] = df_limpio['Producto'].str.title()

# Corrección de tipos
columnas_a_validar = ['Cantidad', 'PrecioUnitario', 'Total']
for col in columnas_a_validar:
    col_corr = col + '_Corregido'
    df_limpio[col_corr] = pd.to_numeric(df_limpio[col], errors='coerce')
    media_col = df_limpio[col_corr].mean()
    df_limpio[col_corr].fillna(media_col, inplace=True)
    df_limpio[col] = df_limpio[col_corr]

# Cálculo de Totales
UMBRAL_DESCUENTO = 1500
TASA_DESCUENTO = 0.10
TASA_IMPUESTO = 0.15 

df_limpio['Descuento'] = np.where(df_limpio['Total'] > UMBRAL_DESCUENTO, df_limpio['Total'] * TASA_DESCUENTO, 0).round(2)
df_limpio['Total_con_descuento'] = (df_limpio['Total'] - df_limpio['Descuento']).round(2)
df_limpio['Impuesto'] = (df_limpio['Total_con_descuento'] * TASA_IMPUESTO).round(2)
df_limpio['Total_Final'] = (df_limpio['Total_con_descuento'] + df_limpio['Impuesto']).round(2)



# 1. Definir los niveles de agrupación
niveles_agrupacion = ['Cliente', 'Producto']

# 2. Agrupar por los dos niveles y sumar la columna 'Total_Final'
df_agrupado_multinivel = df_limpio.groupby(niveles_agrupacion)['Total_Final'].sum()

# Opcional: Convertir el resultado a DataFrame y renombrar la columna para claridad
df_resultado = df_agrupado_multinivel.reset_index(name='Gasto_Total_Final')

# 3. Mostrar los primeros registros
print("=" * 60)
print("Agrupación Multinivel por Cliente y Producto")
print("=" * 60)
print("Muestra de Gasto Total Final por Cliente y Producto:")

# Mostrar el resultado (los 10 principales registros)
print(df_resultado.head(10))
print("-" * 60)