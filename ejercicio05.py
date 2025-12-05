import pandas as pd
import numpy as np
import io

# Cargar el archivo y aplicar la limpieza y cálculos previos (para un estado consistente)
df = pd.read_csv("ventas.csv")
# --- CORRECCIÓN: Usar .copy() después de la limpieza inicial ---
df_limpio = df.dropna().drop_duplicates().copy()

# Normalización de texto (Ej. 2)
df_limpio['Cliente'] = df_limpio['Cliente'].str.title()
df_limpio['Producto'] = df_limpio['Producto'].str.title()

# Recálculo de campos dependientes (Ej. 3) y corrección de tipos (Ej. 4)
columnas_a_validar = ['Cantidad', 'PrecioUnitario', 'Total']
for col in columnas_a_validar:
    col_corr = col + '_Corregido'
    df_limpio[col_corr] = pd.to_numeric(df_limpio[col], errors='coerce')
    media_col = df_limpio[col_corr].mean()
    df_limpio[col_corr].fillna(media_col, inplace=True)
    df_limpio[col] = df_limpio[col_corr] # Sobrescribir con el valor corregido

UMBRAL_DESCUENTO = 1500
TASA_DESCUENTO = 0.10
df_limpio['Descuento'] = np.where(df_limpio['Total'] > UMBRAL_DESCUENTO, df_limpio['Total'] * TASA_DESCUENTO, 0).round(2)
df_limpio['Total_con_descuento'] = (df_limpio['Total'] - df_limpio['Descuento']).round(2)

# --- EJERCICIO 5 ---
TASA_IMPUESTO = 0.15 

# 1. Crear la columna 'Impuesto'
df_limpio['Impuesto'] = (df_limpio['Total_con_descuento'] * TASA_IMPUESTO).round(2)

# 2. Crear la columna 'Total_Final'
df_limpio['Total_Final'] = (df_limpio['Total_con_descuento'] + df_limpio['Impuesto']).round(2)

# 3. Clasificación de rangos de venta
RANGO_BAJO_MAX = 1000  
RANGO_MEDIO_MAX = 3000 

condiciones = [
    (df_limpio['Total_Final'] <= RANGO_BAJO_MAX),
    (df_limpio['Total_Final'] > RANGO_BAJO_MAX) & (df_limpio['Total_Final'] <= RANGO_MEDIO_MAX),
    (df_limpio['Total_Final'] > RANGO_MEDIO_MAX)
]

etiquetas = ['Bajo', 'Medio', 'Alto']

df_limpio['Rango_Venta'] = np.select(condiciones, etiquetas)

print("Código sin Advertencias (SettingWithCopyWarning resuelto)")

print(df_limpio[['Total', 'Descuento', 'Total_Final', 'Rango_Venta']].head(5))