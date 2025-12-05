import pandas as pd
import io


df = pd.read_csv("ventas.csv")
df_limpio = df.dropna().drop_duplicates()


print("Valores Iniciales (Muestra)")
print("---")
print("Clientes Antes:")
print(df_limpio['Cliente'].head().tolist())
print("\nProductos Antes:")
print(df_limpio['Producto'].head().tolist())
print("-" * 40)



df_limpio['Cliente_Normalizado'] = df_limpio['Cliente'].str.title()
df_limpio['Producto_Normalizado'] = df_limpio['Producto'].str.title()


print("Valores Normalizados (Muestra)")
print("---")
print("Clientes Después:")
print(df_limpio['Cliente_Normalizado'].head().tolist())
print("\nProductos Después:")
print(df_limpio['Producto_Normalizado'].head().tolist())
print("-" * 40)


print("Comparación en el DataFrame (Top 5)")
print(df_limpio[['Cliente', 'Cliente_Normalizado', 'Producto', 'Producto_Normalizado']].head())