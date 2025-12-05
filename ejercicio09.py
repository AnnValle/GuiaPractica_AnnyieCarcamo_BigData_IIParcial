import pandas as pd
import io

# Definimos el tamaño del bloque
CHUNK_SIZE = 100 
total_registros_procesados = 0
numero_chunk = 0

print(f"Iniciando Lectura por Chunks (Tamaño de Bloque: {CHUNK_SIZE})")
print("-" * 50)

# 1. Leer el archivo usando chunksize
# Esto devuelve un iterador (TextFileReader) en lugar de un solo DataFrame
try:
    chunk_iterator = pd.read_csv("ventas.csv", chunksize=CHUNK_SIZE)
except FileNotFoundError:
    print("ERROR: El archivo 'ventas.csv' no se encuentra.")
    chunk_iterator = []

# 2. Iterar sobre los bloques y contar los registros
for chunk in chunk_iterator:
    numero_chunk += 1
    # Contar los registros en el chunk actual
    registros_en_chunk = len(chunk)
    total_registros_procesados += registros_en_chunk
    
    print(f"Bloque {numero_chunk}: {registros_en_chunk} registros procesados.")
    # Opcionalmente, aquí se podría aplicar cualquier limpieza o transformación
    # (e.g., chunk.dropna(), chunk['Total'].sum(), etc.)

# 3. Mostrar el total final
print("-" * 50)
print(f"LECTURA FINALIZADA.**")
print(f"Se procesaron un total de {numero_chunk} bloques.")
print(f"**Total final de registros procesados:** {total_registros_procesados}")