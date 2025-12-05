import pandas as pd
import io

# 1. Definimos el tamaño del bloque (chunk)
CHUNK_SIZE = 100 

# Lista para almacenar cada DataFrame (chunk)
list_of_chunks = []

print(f"Unificación de DataFrames por Chunks (Bloque: {CHUNK_SIZE})")
print("-" * 70)

# 2. Leer el archivo usando chunksize
try:
    chunk_iterator = pd.read_csv("ventas.csv", chunksize=CHUNK_SIZE)
except FileNotFoundError:
    print("ERROR: El archivo 'ventas.csv' no se encuentra.")
    chunk_iterator = []

# 3. Iterar sobre los bloques y acumularlos
numero_chunk = 0
for chunk in chunk_iterator:
    numero_chunk += 1
    # Añadir el chunk (que es un DataFrame) a la lista
    list_of_chunks.append(chunk)
    print(f"Bloque {numero_chunk} leído y almacenado ({len(chunk)} registros).")

# 4. Concatenar los chunks para formar el DataFrame final
df_final_unificado = pd.concat(list_of_chunks)

# 5. Mostrar el DataFrame resultante
print("-" * 70)
print("Proceso de unificación finalizado.**")
print(f"Total de bloques leídos: {numero_chunk}")
print(f"Total final de registros en el DataFrame unificado: {len(df_final_unificado)}")
print("-" * 70)

# Mostrar las primeras filas del DataFrame resultante
print("Primeras 5 Filas del DataFrame Unificado:")
print(df_final_unificado.head())
print("-" * 70)