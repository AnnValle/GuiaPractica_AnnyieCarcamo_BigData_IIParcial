import pandas as pd
import numpy as np
import io


df = pd.read_csv("ventas.csv")
df_limpio = df.dropna().drop_duplicates()
df_limpio['Cliente'] = df_limpio['Cliente'].str.title()
df_limpio['Producto'] = df_limpio['Producto'].str.title()


UMBRAL_DESCUENTO = 1500  # Total mínimo para obtener el descuento
TASA_DESCUENTO = 0.10    # 10% de descuento



df_limpio['Descuento'] = np.where(
    df_limpio['Total'] > UMBRAL_DESCUENTO,
    df_limpio['Total'] * TASA_DESCUENTO,
    0
).round(2) 



df_limpio['Total_con_descuento'] = (df_limpio['Total'] - df_limpio['Descuento']).round(2)


print("Filas con las Nuevas Columnas 'Descuento' y 'Total_con_descuento'")
print("---")
print(df_limpio[['Fecha', 'Cliente', 'Producto', 'Total', 'Descuento', 'Total_con_descuento']].head(10))
print("-" * 70)