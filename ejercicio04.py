import pandas as pd
import numpy as np
import io


df = pd.read_csv("ventas.csv")
df_limpio = df.dropna().drop_duplicates().copy() # Usamos .copy() para evitar SettingWithCopyWarning
df_limpio['Cliente'] = df_limpio['Cliente'].str.title()
df_limpio['Producto'] = df_limpio['Producto'].str.title()
UMBRAL_DESCUENTO = 1500
TASA_DESCUENTO = 0.10
df_limpio['Descuento'] = np.where(df_limpio['Total'] > UMBRAL_DESCUENTO, df_limpio['Total'] * TASA_DESCUENTO, 0).round(2)
df_limpio['Total_con_descuento'] = (df_limpio['Total'] - df_limpio['Descuento']).round(2)


columnas_a_validar = ['Cantidad', 'PrecioUnitario', 'Total']

print("Tipos de Datos Iniciales")
print("---")
print(df_limpio[columnas_a_validar].dtypes)
print("-" * 30)


for col in columnas_a_validar:
    
    df_limpio[col + '_Corregido'] = pd.to_numeric(df_limpio[col], errors='coerce')
    
   
    nans_corregidos = df_limpio[col + '_Corregido'].isnull().sum()
    print(f" Columna **'{col}'**: **{nans_corregidos}** valor(es) no numérico(s) detectado(s).")

print("-" * 30)


print("Reemplazo de Valores Inválidos")
for col in columnas_a_validar:
    col_corr = col + '_Corregido'
    
    
    media_col = df_limpio[col_corr].mean()
    
    
    df_limpio[col_corr].fillna(media_col, inplace=True)
    
    
    nans_finales = df_limpio[col_corr].isnull().sum()
    print(f"Columna **'{col}'**: Media usada para reemplazo: **{media_col:.2f}**. NaN(s) restantes: **{nans_finales}**.")
    

df_limpio['Cantidad'] = df_limpio['Cantidad_Corregido']
df_limpio['PrecioUnitario'] = df_limpio['PrecioUnitario_Corregido']
df_limpio['Total'] = df_limpio['Total_Corregido']


print("-" * 30)
print("Tipos de Datos Finales")
print("---")
print(df_limpio[['Cantidad', 'PrecioUnitario', 'Total']].dtypes)