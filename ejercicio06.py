import pandas as pd
import numpy as np
import io

df = pd.read_csv("ventas.csv")
df_limpio = df.dropna().drop_duplicates().copy()

df_limpio['Cliente'] = df_limpio['Cliente'].str.title()
df_limpio['Producto'] = df_limpio['Producto'].str.title()

columnas_a_validar = ['Cantidad', 'PrecioUnitario', 'Total']
for col in columnas_a_validar:
    col_corr = col + '_Corregido'
    df_limpio[col_corr] = pd.to_numeric(df_limpio[col], errors='coerce')
    media_col = df_limpio[col_corr].mean()
    df_limpio[col_corr].fillna(media_col, inplace=True)
    df_limpio[col] = df_limpio[col_corr]

UMBRAL_DESCUENTO = 1500
TASA_DESCUENTO = 0.10
df_limpio['Descuento'] = np.where(df_limpio['Total'] > UMBRAL_DESCUENTO, df_limpio['Total'] * TASA_DESCUENTO, 0).round(2)
df_limpio['Total_con_descuento'] = (df_limpio['Total'] - df_limpio['Descuento']).round(2)
TASA_IMPUESTO = 0.15 
df_limpio['Impuesto'] = (df_limpio['Total_con_descuento'] * TASA_IMPUESTO).round(2)
df_limpio['Total_Final'] = (df_limpio['Total_con_descuento'] + df_limpio['Impuesto']).round(2)



UMBRAL_FILTRO = 3500


df_filtrado = df_limpio[df_limpio['Total_Final'] > UMBRAL_FILTRO].copy()


df_ordenado = df_filtrado.sort_values(by='Total_Final', ascending=False)


print(f"Transacciones con Total Final Mayor a ${UMBRAL_FILTRO}")
print("---")
print(f"Número total de registros filtrados: {len(df_ordenado)}")
print("-" * 50)

columnas_resultado = ['Fecha', 'Cliente', 'Producto', 'Cantidad', 'Total', 'Descuento', 'Total_Final']
print(df_ordenado[columnas_resultado])