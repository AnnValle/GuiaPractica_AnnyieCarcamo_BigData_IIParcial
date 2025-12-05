import pandas as pd
import io


df = pd.read_csv("ventas.csv")


print(f"Registros iniciales: {len(df)}")
print("-" * 30)


nulos_por_columna = df.isnull().sum()
total_nulos = nulos_por_columna.sum()
print(f"Valores nulos detectados (por columna):\n{nulos_por_columna[nulos_por_columna > 0]}")
print(f"Total de valores nulos en el conjunto de datos: {total_nulos}")


df_limpio = df.dropna()
print(f"Registros eliminados por nulos: {len(df) - len(df_limpio)}")
print(f"Registros después de eliminar nulos: {len(df_limpio)}")
print("-" * 30)


duplicados_antes = df_limpio.duplicated().sum()
print(f" Filas duplicadas detectadas: {duplicados_antes}")


df_limpio = df_limpio.drop_duplicates()
duplicados_despues = df_limpio.duplicated().sum()
print(f"Registros eliminados por duplicidad: {duplicados_antes - duplicados_despues}")
print("-" * 30)



print(f"TOTAL FINAL DE REGISTROS LIMPIOS: {len(df_limpio)}")