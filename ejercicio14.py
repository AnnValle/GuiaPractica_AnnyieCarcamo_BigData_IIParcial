import pandas as pd
import time
import io
import numpy as np

# Definimos una función de limpieza y suma que aplicaremos a ambos métodos
def limpiar_y_sumar(df):
    """Limpia los valores no numéricos en la columna 'Total' y retorna la suma."""
    # Intentar convertir a numérico, forzando errores a NaN
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    # Reemplazar NaN con la media de los valores válidos del DataFrame/Chunk
    df['Total'].fillna(df['Total'].mean(), inplace=True)
    return df['Total'].sum()


print("MÉTODO 1: Lectura y Procesamiento Normal")
inicio_normal = time.time()

try:
    # 1. Leer el archivo completo
    df_normal = pd.read_csv("ventas.csv", usecols=['Total'])
    
    # 2. Limpiar y sumar
    total_normal = limpiar_y_sumar(df_normal)
    
except FileNotFoundError:
    print("ERROR: El archivo 'ventas.csv' no se encuentra.")
    total_normal = 0.0

fin_normal = time.time()
tiempo_normal = fin_normal - inicio_normal



CHUNK_SIZE = 100 
total_chunk = 0.0

print("\nMÉTODO 2: Lectura y Procesamiento por Chunks")
inicio_chunk = time.time()

try:
    # 1. Crear el iterador de chunks
    chunk_iterator = pd.read_csv("ventas.csv", chunksize=CHUNK_SIZE, usecols=['Total'])
    
    # 2. Iterar sobre los bloques, limpiar y acumular la suma
    for chunk in chunk_iterator:
        total_chunk += limpiar_y_sumar(chunk)
        
except FileNotFoundError:
    print("ERROR: El archivo 'ventas.csv' no se encuentra.")
    total_chunk = 0.0

fin_chunk = time.time()
tiempo_chunk = fin_chunk - inicio_chunk





print("COMPARACIÓN DE RENDIMIENTO")

# El resultado de la suma debe ser el mismo en ambos métodos
print(f"Suma Total Global (Normal):   ${total_normal:,.2f}")
print(f"Suma Total Global (Chunks):  ${total_chunk:,.2f}")


# Comparar los tiempos de ejecución
print(f"Tiempo de Ejecución (Normal): {tiempo_normal:.6f} segundos")
print(f"Tiempo de Ejecución (Chunks): {tiempo_chunk:.6f} segundos")



# Conclusión
if tiempo_chunk < tiempo_normal:
    print("CONCLUSIÓN: El método por Chunks fue más rápido en este caso.")
else:
    print("CONCLUSIÓN: El método Normal (carga completa) fue más rápido en este caso.")

