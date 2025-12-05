import pandas as pd
import numpy as np
import io



df = pd.read_csv("ventas.csv")
df_limpio = df.dropna().drop_duplicates().copy()

# Normalización y Corrección de Tipos
df_limpio['Cliente'] = df_limpio['Cliente'].str.title()
df_limpio['Producto'] = df_limpio['Producto'].str.title()

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

df_limpio['Fecha'] = pd.to_datetime(df_limpio['Fecha'])



# 1. Definir los parámetros de filtrado
RANGO_MIN = 1500
RANGO_MAX = 3000
PRODUCTO_ESPECIFICO = 'Teclado Mecánico'
CLIENTES_SELECCIONADOS = ['Lucía Torres', 'Luis Hernández']

# 2. Construir las tres condiciones lógicas
filtro_rango = (df_limpio['Total_Final'] >= RANGO_MIN) & (df_limpio['Total_Final'] <= RANGO_MAX)
filtro_producto = df_limpio['Producto'] == PRODUCTO_ESPECIFICO
filtro_clientes = df_limpio['Cliente'].isin(CLIENTES_SELECCIONADOS)

# 3. Aplicar el filtrado múltiple usando el operador AND (&)
df_filtrado_multiple = df_limpio[
    filtro_rango & filtro_producto & filtro_clientes
].copy()


# 4. Mostrar el resultado
print("=" * 90)
print("## Resultados del Filtrado Múltiple (AND)")
print("=" * 90)
print(f"**Condiciones:**")
print(f"* Total Final: Entre ${RANGO_MIN:.2f} y ${RANGO_MAX:.2f}")
print(f"* Producto: '{PRODUCTO_ESPECIFICO}'")
print(f"* Clientes: {CLIENTES_SELECCIONADOS}")
print("-" * 90)

columnas_resultado = ['Fecha', 'Cliente', 'Producto', 'Total_Final']

if len(df_filtrado_multiple) > 0:
    print(f"**Se encontraron {len(df_filtrado_multiple)} transacciones que cumplen todos los criterios.**\n")
    print(df_filtrado_multiple[columnas_resultado].sort_values(by='Total_Final', ascending=False))
else:
    print("No se encontró ninguna transacción que cumpliera simultáneamente las tres condiciones.")

print("=" * 90)